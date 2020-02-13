import socket
import json
from time import sleep

value = 1
package = {"event": "Hello, world!",
           "metric_value": value,
           "sourcetype": "json",
           "source": "testsrc"}

HOST = 'localhost'    # The remote host
PORT = 9000           # The same port as used by the server

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        while True:

            package['metric_value'] = value
            value += 1
            string_package = json.dumps(package)
            print(string_package)
            s.send(string_package.encode())

            sleep(0.1)

    except ConnectionRefusedError as e:
        print(e)

    except ConnectionResetError as e:
        print(e)

    except ConnectionAbortedError as e:
        print(e)

    except OSError as e:
        print(e)


def socket_connect(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def socket_send(s, package):
    string_package = json.dumps(package)
    print(string_package)
    s.send(string_package.encode())

