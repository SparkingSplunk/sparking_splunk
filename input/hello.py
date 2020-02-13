from flask import Flask
from flask import render_template


clicks={"blue":0}


app=Flask(__name__)

@app.route('/')
def test():
    return render_template("index.html")

@app.route('/sendClick')
def sendClick():
    #clicks["blue"]+=1
    mentor = request.form[""]
    bootcamper = request.form["b"]
  
  


if __name__=="__main__":
    app.run(host="127.0.0.1", port=5000, debug=None)