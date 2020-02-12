from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import socket
import json
from process_rdd import process_rdd


def process_send_rdd(rdd):
    """Processes and sends the RDD as a string through a specified port."""

    def send_event(event):
        HOST = 'localhost'  # The remote host
        PORT = 9005  # The same port as used by the server

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        string_package = json.dumps(event) + '\n'
        print(string_package)
        s.send(string_package.encode())

    # Process the RDD
    output_dict = process_rdd(rdd)
    send_event(output_dict)


# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[*]", "NetworkWordCount")
sc.setLogLevel('ERROR')
ssc = StreamingContext(sc, batchDuration=0.1)

# Create a DStream that will connect to hostname:port, like localhost:9999
dstream = ssc.socketTextStream("localhost", 9001)

# Extract the numerical values
value_stream = dstream.map(lambda event: json.loads(event)["metric_value"])

# Create a windowed data stream
windowed_stream = value_stream.window(windowDuration=5, slideDuration=0.1)

# Process and send each event through the specified port
windowed_stream.foreachRDD(process_send_rdd)

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
