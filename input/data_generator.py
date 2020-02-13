import socket
import json
from time import sleep


class Listener:
    def __init__(self,HOST, PORT):
        self.host=HOST
        self.port=PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    
    def generator(self,value):

        package = {
            "metric_label": "CPU",
            "metric_value": value,
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