import paho.mqtt.publish as mqtt_publish
from pynput import keyboard
import uuid

# MQTT Configuration
MQTT_BROKER_HOST = "192.168.0.105"
MQTT_TOPIC_CONTROLLER = "/rover/controller"

# Generate a random user ID
user_id = str(uuid.uuid4())

# Define the MQTT message payload for each key, including speed and user ID
KEY_MAPPINGS = {
    keyboard.Key.up: f'{{"user_id": "{user_id}", "direction": "FORWARD", "speed": 100}}',
    keyboard.Key.down: f'{{"user_id": "{user_id}", "direction": "BACKWARD", "speed": 100}}',
    keyboard.Key.left: f'{{"user_id": "{user_id}", "direction": "LEFT", "speed": 100}}',
    keyboard.Key.right: f'{{"user_id": "{user_id}", "direction": "RIGHT", "speed": 100}}'
}

def on_key_press(key):
    if key in KEY_MAPPINGS:
        payload = KEY_MAPPINGS[key]
        mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=payload, hostname=MQTT_BROKER_HOST)
        print(f"Published: {payload}")

def on_key_release(key):
    if key in KEY_MAPPINGS:
        payload = f'{{"user_id": "{user_id}", "direction": "STOP"}}'
        mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=payload, hostname=MQTT_BROKER_HOST)
        print(f"Published: {payload}")

# Start listening to keyboard events
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
