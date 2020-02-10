import socket
from time import sleep

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9999         # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            sleep(1)
            conn.send(b"Hello\n")
