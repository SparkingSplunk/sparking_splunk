from flask import Flask
from flask import render_template
from data_generator import Listener
import os
import threading
from time import sleep
click = 0

listener = Listener("localhost", 9111, 0)

app=Flask(__name__)

@app.route('/')
def test():
    return render_template("index.html")


@app.route('/up', methods=["POST"])
def up():

    listener.clickme('up')
    return "up"

@app.route('/down', methods=["POST"])
def down():
    listener.clickme('down')
    return "down"


if __name__=="__main__":


    # myThread = threading.Timer(3, ggggg, [listener])  # timer is set to 3 seconds
    # myThread.start()


    app.run(host="127.0.0.1", port=9999, debug=None)

