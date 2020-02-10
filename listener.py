import socket
from time import sleep
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9999         # Port to listen on (non-privileged ports are > 1023)

while True:
    print("Trying to connect")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()
            print("Connected to socket")
            with conn:
                print('Connected by', addr)
                while True:
                    sleep(1)
                    package = conn.recv(1024)
                    print(package)
                    # conn.send(b"Hello\n")
    except:
        print("Connection lost")
