from gpiozero import LED, RGBLED, Buzzer
import time
from flask import Flask, request

app = Flask(__name__)

leds = {
    'red' : LED(22),
    'green' : LED(23),
    'blue' : LED(24)
}

rgb = RGBLED(red=9, green=10, blue=11, active_high=False)
buzzer = Buzzer(26)

@app.route('/flash/<color>')
def flashred(color):
    pin = leds.get(color)
    pin.on()
    time.sleep(1)
    pin.off()

if __name__ == "__main__":
    app.run(host='0.0.0.0')