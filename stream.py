from pyspark import SparkContext
from pyspark.streaming import StreamingContext

import socket
import json

# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[*]", "NetworkWordCount")
sc.setLogLevel('ERROR')
ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
events = ssc.socketTextStream("localhost", 9001)

events_dict = events.map(lambda event: json.loads(events))
events_dict.pprint()




# HOST = 'localhost'    # The remote host
# PORT = 9005           # The same port as used by the server
#
# while True:
#     try:
#         s.connect((HOST, PORT))
#
#         while True:
#
#             package['metric_value'] = value
#             value += 1
#             string_package = json.dumps(package) + '\n'
#             print(string_package)
#
#             s.send(string_package.encode())
#             sleep(1)
#
#     except ConnectionRefusedError as e:
#         print(e)
#
#     except ConnectionResetError as e:
#         print(e)
#
#     except ConnectionAbortedError as e:
#         print(e)





# # Split each line into words
# words = lines.flatMap(lambda line: line.split(" "))
#
# # Count each word in each batch
# pairs = words.map(lambda word: (word, 1))
# wordCounts = pairs.reduceByKey(lambda x, y: x + y)
#
# # Print the first ten elements of each RDD generated in this DStream to the console
# wordCounts.pprint()



ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
