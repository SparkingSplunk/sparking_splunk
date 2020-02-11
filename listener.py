import socket
import json

INPUT_HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
INPUT_PORT = 9000         # Port to listen on (non-privileged ports are > 1023)

OUTPUT_HOST = '127.0.0.1'
OUTPUT_PORT = 9001

while True:
    print("Trying to reconnect ...")
    try:
        input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        input_socket.bind((INPUT_HOST, INPUT_PORT))
        output_socket.bind((OUTPUT_HOST, OUTPUT_PORT))

        input_socket.listen(1)
        output_socket.listen(1)

        print("Waiting for input connection ...")
        input_conn, input_addr = input_socket.accept()
        print("Input connected.")

        print("Waiting for output connection ...")
        output_conn, output_addr = output_socket.accept()
        print("Output connected.")

        with input_conn:
            print('Input connected by', input_addr)
            with output_conn:
                print('Input connected by', output_addr)

                while True:
                    package = input_conn.recv(1024)
                    print(package)
                    output_conn.send(package)

        input_socket.close()
        output_socket.close()

    except ConnectionRefusedError as e:
        print(e)

    except ConnectionResetError as e:
        print(e)

    except ConnectionAbortedError as e:
        print(e)
