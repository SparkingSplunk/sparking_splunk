import socket

INPUT_HOST = 'localhost'  # Standard loopback interface address (localhost)
INPUT_PORT = 9996         # Port to listen on (non-privileged ports are > 1023)

OUTPUT_HOST = 'localhost'
OUTPUT_PORT = 9998

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
                print('put connected by', output_addr)

                while True:
                    package = input_conn.recv(1024)
                    if not package:
                        break
                    print(package)
                    output_conn.send(package)

        input_socket.close()
        output_socket.close()

    except ConnectionResetError as e:
        print(e)

    except ConnectionAbortedError as e:
        print(e)