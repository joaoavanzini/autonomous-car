import paho.mqtt.publish as mqtt_publish
from pynput import keyboard
import uuid
import time
import json

# MQTT Configuration
MQTT_BROKER_HOST = "192.168.0.105"
MQTT_TOPIC_CONTROLLER = "/rover/controller"

# Generate a random user ID
user_id = str(uuid.uuid4())

def generate_message_id():
    return str(uuid.uuid4())

# Define the MQTT message payload for each key, including speed, user_id, and message_id
def create_payload(direction):
    message_id = generate_message_id()
    timestamp_micros = int(time.time() * 1e6)  # Microseconds since epoch
    payload = {
        "user_id": user_id,
        "message_id": message_id,
        "direction": direction,
        "speed": 100,
        "timestamp_micros": timestamp_micros  # Include micros
    }
    return payload

KEY_MAPPINGS = {
    keyboard.Key.up: create_payload("FORWARD"),
    keyboard.Key.down: create_payload("BACKWARD"),
    keyboard.Key.left: create_payload("LEFT"),
    keyboard.Key.right: create_payload("RIGHT")
}

def on_key_press(key):
    if key in KEY_MAPPINGS:
        payload = KEY_MAPPINGS[key]
        mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=json.dumps(payload), hostname=MQTT_BROKER_HOST)
        print(f"Published: {payload}")

def on_key_release(key):
    if key in KEY_MAPPINGS:
        payload = {
            "user_id": user_id,
            "message_id": generate_message_id(),
            "direction": "STOP",
            "speed": 0,
            "timestamp_micros": int(time.time() * 1e6)  # Include micros
        }
        mqtt_publish.single(MQTT_TOPIC_CONTROLLER, payload=json.dumps(payload), hostname=MQTT_BROKER_HOST)
        print(f"Published: {payload}")

# Start listening to keyboard events
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
