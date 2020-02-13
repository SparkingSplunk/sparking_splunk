from flask import Flask
from flask import render_template
from data_generator import Listener
import os


Listener=Listener("localhost", 9111)

# magic_value = 0

app=Flask(__name__)

# def magic_funtion():
#

@app.route('/')
def test():
    return render_template("index.html")


@app.route('/up', methods=["POST"])
def up():

    Listener.clickme("up")
    return "up"

@app.route('/down', methods=["POST"])
def down():
    while(1):
        x = 1
    Listener.clickme("down")
    return "down"


if __name__=="__main__":
    app.run(host="127.0.0.1", port=9999, debug=None)