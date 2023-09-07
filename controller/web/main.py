from flask import Flask, render_template
import paho.mqtt.publish as mqtt_publish
from pynput import keyboard

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER_HOST = "192.168.0.104"
MQTT_TOPIC_CONTROLLER = "/controller"

# Define the MQTT message payload for each key, including speed
KEY_MAPPINGS = {
    keyboard.Key.up: '{"direction": "BACKWARD", "speed": 100}',
    keyboard.Key.down: '{"direction": "FORWARD", "speed": 100}',
    keyboard.Key.left: '{"direction": "LEFT", "speed": 100}',
    keyboard.Key.right: '{"direction": "RIGHT", "speed": 100}'
}

def on_key_press(key):
    if key in KEY_MAPPINGS:
        payload = KEY_MAPPINGS[key]
        mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=payload, hostname=MQTT_BROKER_HOST)
        print(f"Published: {payload}")

def on_key_release(key):
    if key in KEY_MAPPINGS:
        payload = '{"direction": "STOP"}'
        mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=payload, hostname=MQTT_BROKER_HOST)
        print(f"Published: {payload}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        app.run(host='0.0.0.0', debug=True)
