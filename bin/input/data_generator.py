import socket
import json
from time import sleep


package = {"metric_value": "NaN"}

class Listener:
    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((HOST,PORT))
        self.s.connect((HOST, PORT))
        self.value=0

    def send(self):

        try:
            package['metric_value'] = self.value
            string_package = json.dumps(package) + '\n'
            print(string_package)
            self.s.send(string_package.encode())
            sleep(0.1)

        except ConnectionRefusedError as e:
            print(e)

        except ConnectionResetError as e:
            print(e)

        except ConnectionAbortedError as e:
            print(e)

        except OSError as e:
            print(e)

    def clickme(self, action):
        if action=="up":
            self.value+=1
        elif action=="down":
            self.value-=1
        else:
            print("not found")
        self.send()


if __name__ == '__main__':
    listener = Listener("localhost", 9111)

    while True:
        sleep(0.5)
        listener.send()



