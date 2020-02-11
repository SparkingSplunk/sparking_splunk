# Echo client program
import socket
import sys
import json
from time import sleep

value = 1
package = {
    "metric_label": "CPU",
    "metric_value": value,
    "host": "Erics-MacBook-Pro-34.local",
    "source": "Splunk_Index",
    "source_type": "json"
}

HOST = 'localhost'    # The remote host
PORT = 9000           # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        s.connect((HOST, PORT))

        while True:

            package['metric_value'] = value
            value += 1
            stringpackage = json.dumps(package) + '\n'
            print(stringpackage)

            s.send(stringpackage.encode())
            sleep(1)

    except ConnectionRefusedError as e:
        print(e)

    except ConnectionResetError as e:
        print(e)

    except ConnectionAbortedError as e:
        print(e)





#
#
# if s is None:
#     print('could not open socket')
#     sys.exit(1)
# with s:
#     while True:
#
#         package['metric_value'] = value
#         value += 1
#         s.send((json.dumps(package) + '\n').encode())
#         sleep(1)
#         # data = s.recv(1024)
#
# # print('Received', repr(data))
