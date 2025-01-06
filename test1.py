import RPi.GPIO as io
import time
from flask import Flask, render_template

app = Flask(__name__)
io.setmode(io.BCM)
led1 = 27
io.setup(led1, io.OUT)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/flash')
def flash():
    io.output(led1, True)
    time.sleep(1)
    io.output(led1, False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)