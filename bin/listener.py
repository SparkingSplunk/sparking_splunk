import socket
import json
INPUT_HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
INPUT_PORT = 9111         # Port to listen on (non-privileged ports are > 1023)

OUTPUT_HOST = '127.0.0.1'
OUTPUT_PORT = 9001

last_package = json.dumps({
    "metric_label": "CPU",
    "metric_value": 0,
    "host": "Erics-MacBook-Pro-34.local",
    "source": "Splunk_Index",
    "source_type": "json"
}) + '\n'

while True:
    print("Trying to reconnect ...")
    try:
        input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        input_socket.bind((INPUT_HOST, INPUT_PORT))
        output_socket.bind((OUTPUT_HOST, OUTPUT_PORT))

        input_socket.listen(2)
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
                print('Output connected by', output_addr)

                while True:
                    package = input_conn.recv(1024)
                    print(package)
                    if json.loads(package[0:-1])['metric_value'] == 'NaN':
                        output_conn.send(last_package)
                    else:
                        output_conn.send(package)
                        print(package)
                        last_package = package

        input_socket.close()
        output_socket.close()

    except ConnectionResetError as e:
        print(e)

    except ConnectionAbortedError as e:
        print(e)