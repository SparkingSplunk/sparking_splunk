def process_rdd(rdd):
    """RDD processing function which returns a dictionary of the results."""
    output = {}

    window_array = rdd.collect()
    window_length = len(window_array)

    if window_length == 0:
        return

    if window_length == 0:
        output["mean"] = 0
        output["meanAbsDev"] = 0

    else:
        average = sum(window_array) / len(window_array)
        output["mean"] = average
        mean_abs_dev = sum(abs(x - average) for x in window_array) / window_length
        output["meanAbsDev"] = mean_abs_dev
        output["lower"] = [average - n * mean_abs_dev for n in range(1, 5)]
        output["upper"] = [average + n * mean_abs_dev for n in range(1, 5)]

        print("List", window_array)
        print("List Length", window_length)
        print("Average", average)
        print("Mean Absolute Deviation", mean_abs_dev)

    return output
