from pyspark import SparkContext
from pyspark.streaming import StreamingContext

import socket
import json




def process_event(event):
    """Processing function for each event."""

    event_dict = json.loads(event)

    event_dict["metric_value"] = 1000

    processed_event = json.dumps(event_dict)
    return processed_event


def send_rdd(rdd):
    """Sends the RDD as a string through a specified port."""

    def send_event(event):
        HOST = 'localhost'  # The remote host
        PORT = 9005  # The same port as used by the server

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        string_package = json.dumps([event]) + '\n'
        print(string_package)
        s.send(string_package.encode())

    rdd.foreach(send_event)


# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[*]", "NetworkWordCount")
sc.setLogLevel('ERROR')
ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
dstream = ssc.socketTextStream("localhost", 9996)

# Run the processing function on the datastream
processed_dstream = dstream.map(process_event)

# Send each event through the specified port
processed_dstream.foreachRDD(send_rdd)

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
