import socket
import json
from time import sleep


package = {
    "metric_label": "CPU",
    "metric_value": 0,
    "host": "Erics-MacBook-Pro-34.local",
    "source": "Splunk_Index",
    "source_type": "json"
}

class Listener:
    def __init__(self, HOST, PORT, value):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((HOST,PORT))
        self.s.connect((HOST, PORT))
        self.value=value

    def send(self):

        try:
            if self.value == "NaN":
                self.s.send("NaN".encode())
            else:
                package['metric_value'] = self.value
                string_package = json.dumps(package) + '\n'
                print(string_package)
                self.s.send(string_package.encode())

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
    package = {"metric_value": "NaN"}
    listener = Listener("localhost", 9111, "NaN")

    while True:
        sleep(0.1)
        listener.send()



