# Echo client program
import socket
import sys
import json
from time import sleep

package = {
    "metric_label" : "CPU",
    "metric_value" : "95",
    "host" : "Erics-MacBook-Pro-34.local",
    "source" : "Splunk_Index",
    "source_type" : "json"
}

HOST = 'localhost'    # The remote host
PORT = 9999              # The same port as used by the server
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
with s:
    while True:
        s.send(json.dumps(package).encode())
        sleep(1)
        # data = s.recv(1024)

# print('Received', repr(data))
