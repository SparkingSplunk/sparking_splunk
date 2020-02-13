import socket
import json
from time import sleep


#def generator(value, HOST, PORT):
HOST="localhost"
PORT=9111
value=1

package = {
    "metric_label": "CPU",
    "metric_value": value,
    "host": "Erics-MacBook-Pro-34.local",
    "source": "Splunk_Index",
    "source_type": "json"
}

string_package = json.dumps(package) + '\n'


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(string_package)
    s.send(string_package.encode())

    

except ConnectionRefusedError as e:
    print(e)

except ConnectionResetError as e:
    print(e)

except ConnectionAbortedError as e:
    print(e)

except OSError as e:
    print(e)