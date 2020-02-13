from flask import Flask
from flask import render_template
from data_generator import Listener
import os

clicks={"blue":0}
Listener=Listener("localhost", 9111)

app=Flask(__name__)

@app.route('/')
def test():
    return render_template("index.html")


@app.route('/sendClick', methods=['POST'])
def sendClick():
    clicks["blue"]+=1
    
    Listener.generator(clicks["blue"])
    return str(clicks["blue"])


if __name__=="__main__":
    app.run(host="127.0.0.1", port=5000, debug=None)