import json


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
    out["Time"] = ""
    out["alert"] = round(severity * 5)
    out["metric_value"] = value
    out["algorithm"] = ""
    out["source"] = "search_acn_mywizardaiops_stormwatch_execute_algorithms"
    out["source_type"] = "stash"

    return out
