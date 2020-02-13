from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import socket
import json
import time


def stream_config(dstream):

    # Extract the numerical values
    value_stream = dstream.map(lambda event: json.loads(event)["metric_value"])

    # Create a windowed data stream
    windowed_stream = value_stream.window(windowDuration=5, slideDuration=0.1)

    return windowed_stream


def process_rdd(rdd):
    """RDD processing function which returns a dictionary of the results."""
    output = {}

    window_array = rdd.collect()

    window_length = len(window_array)
    if window_length == 0:
        return

    average = sum(window_array) / window_length
    output["mean"] = average
    mean_abs_dev = sum(abs(x - average) for x in window_array) / window_length
    output["meanAbsDev"] = mean_abs_dev
    output["lower"] = [average - n * mean_abs_dev for n in range(1, 5)]
    output["upper"] = [average + n * mean_abs_dev for n in range(1, 5)]

    print("List", window_array)
    print("List Length", window_length)
    print("Average", average)
    print("Mean Absolute Deviation", mean_abs_dev)

    out = {}

    value = window_array[-1]
    severity = min(1, abs(value - average) / (5 * mean_abs_dev))

    out["model_results"] = json.dumps(output) + '\n'
    out["Error"] = ""
    out["host"] = "ANZ"
    out["severity"] = severity
    out["metric_label"] = "Control007"
    out["time"] = round(time.time() * 1000)
    out["alert"] = round(severity * 5)
    out["metric_value"] = value
    out["algorithm"] = ""
    out["source"] = "search_acn_mywizardaiops_stormwatch_execute_algorithms"
    out["source_type"] = "stash"

    return out


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

# Configure the output stream
output_stream = stream_config(dstream)

# Process and send each event through the specified port
output_stream.foreachRDD(process_send_rdd)

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
