from gpiozero import LED, RGBLED
import time
import threading
import json
from flask import Flask, json
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import serial
import threading

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


leds = {
    'red': LED(22),
    'green': LED(23),
    'blue': LED(24)
}

rgbLED = RGBLED(9,10,11, active_high=False)
rgbLED.off()

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
pot_value = None

def read_pico_uart():
    global pot_value

    buffer = ""

    while True:
        try:
            data = ser.read().decode(errors="ignore")
            if data:
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line.isdigit():
                        pot_value = int(line)
        except Exception as e:
            print("UART read error:", e)

def updatePot():
    while True:
        socketio.emit("pot_update", {"value": pot_value})
        time.sleep(0.1)

threading.Thread(target=read_pico_uart, daemon=True).start()
threading.Thread(target=updatePot, daemon=True).start()
    
def flash_led(pin):
    pin.on()
    time.sleep(1)
    pin.off()

@app.route('/flash/<color>')
def flash_color(color):
    pin = leds.get(color)
    if pin:
        threading.Thread(target=flash_led, args=(pin,)).start()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'error': 'Invalid color'}), 400, {'ContentType': 'application/json'}
    
@socketio.on('led_flashing')
def handle_led_flashing(data):
    color = data.get('color')
    pin = leds.get(color)
    if pin:
        threading.Thread(target=flash_led, args=(pin,)).start()
        return {'success': True}
    else:
        return {'success': False, 'error': 'Invalid color'}

@socketio.on('getRGB')
def handle_led_flashing():
    return {'rgb': rgbLED.value}

@socketio.on('setRGB')
def handle_led_flashing(data):
    colors = data.get('colors')
    try:
        rgbLED.color = tuple(colors)
        return {'success': True}
    except:
        return {'success': False, 'error': 'Invalid color'}

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
