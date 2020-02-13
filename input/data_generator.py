import socket
import json
from time import sleep


def generator(value, host, port):
    package = {
        "metric_label": "CPU",
        "metric_value": value,
        "host": "Erics-MacBook-Pro-34.local",
        "source": "Splunk_Index",
        "source_type": "json"
    }

    HOST = host   # The remote host
    PORT = port           # The same port as used by the server


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        package['metric_value'] = value
        value += 1
        string_package = json.dumps(package) + '\n'
        print(string_package)
        s.send(string_package.encode())

        sleep(1)

    except ConnectionRefusedError as e:
        print(e)

    except ConnectionResetError as e:
        print(e)

    except ConnectionAbortedError as e:
        print(e)

    except OSError as e:
        print(e)