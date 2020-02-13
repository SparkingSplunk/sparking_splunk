import socket
import json
from time import sleep


class Listener:
    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((HOST,PORT))
        self.s.connect((HOST, PORT))
        self.value=0

    def clickme(self, action):
        if action=="up":
            self.value+=1
        elif action=="down":
            self.value-=1
        else:
            print("not found")
      
        package = {
            "metric_label": "CPU",
            "metric_value": self.value,
            "host": "Erics-MacBook-Pro-34.local",
            "source": "Splunk_Index",
            "source_type": "json"
        }

        try:
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
