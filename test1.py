from gpiozero import LED
import time
from flask import Flask, json, request, render_template

app = Flask(__name__)
pins = {
    LED(22) : 'red',
    LED(23) : 'green',
    LED(24) : 'blue'
}

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/flash')
def flash():
    colour = request.args.get('colour')
    if colour in pins.values():
        pin = [i for i in pins if pins[i]==colour]
        pin.on()
        time.sleep(1)
        pin.off()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)