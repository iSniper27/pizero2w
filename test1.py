from gpiozero import LED, RGBLED
import time
from flask import Flask, json, request, render_template

app = Flask(__name__)

pins = {
    'red' : LED(22),
    'green' : LED(23),
    'blue' : LED(24),
    'rgb' : RGBLED(red=9, green=10, blue=11, active_high=False)
}

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/light')
def flash():
    type = request.args.get('type')
    try:
        if type == 'led':
            colour = request.args.get('colour')
            pin = pins.get(colour)
            pin.on()
            time.sleep(1)
            pin.off()
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        elif type == 'rgb':
            rgbcode = eval(request.args.get('rgbcode'))
            pins['rgb'].color = rgbcode
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    except:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(host='0.0.0.0')