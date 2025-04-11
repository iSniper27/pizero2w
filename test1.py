from gpiozero import LED, RGBLED, Buzzer
import time
import threading
from flask import Flask, json
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

leds = {
    'red': LED(22),
    'green': LED(23),
    'blue': LED(24)
}

#rgb = RGBLED(red=9, green=10, blue=11, active_high=False)
#buzzer = Buzzer(26)

def flash_led(pin):
    pin.on()
    time.sleep(1)
    pin.off()

@app.route('/flash/<color>')
def flash_color(color):
    pin = leds.get(color)
    if pin:
        socketio.emit('led_flashing', {'color': color})
        threading.Thread(target=flash_led, args=(pin)).start()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'error': 'Invalid color'}), 400, {'ContentType': 'application/json'}

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
