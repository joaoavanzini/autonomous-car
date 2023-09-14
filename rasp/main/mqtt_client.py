import paho.mqtt.client as mqtt
import json
import logging
from config import MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_TOPIC_CONTROLLER, MQTT_TOPIC_STATUS
from rover import Rover
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.rover = Rover()

    def connect(self):
        self.client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

    def subscribe(self):
        self.client.subscribe(MQTT_TOPIC_CONTROLLER)

    def start(self):
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        try:
            data = json.loads(payload)
            direction = data.get('direction', 'STOP')
            speed = data.get('speed', 100)
            user_id = data.get('user_id', '')
            message_id = data.get('message_id', '')

            direction_map = {
                'FORWARD': self.rover.move_forward,
                'BACKWARD': self.rover.move_backward,
                'RIGHT': self.rover.turn_right,
                'LEFT': self.rover.turn_left,
                'STOP': self.rover.stop
            }

            action = direction_map.get(direction)
            if action:
                action(speed)
            else:
                error_message = f"Invalid direction: {direction}"
                logger.error(error_message)
                self.report_error(error_message)

            timestamp_micros = data.get('timestamp_micros', 0)
            timestamp_seconds = timestamp_micros / 1e6  # Convert micros to seconds

            timestamp_data = {
                "user_id": user_id,
                "message_id": message_id,
                "timestamp_micros": timestamp_micros,
                "timestamp_seconds": timestamp_seconds
            }
            timestamp_json = json.dumps(timestamp_data)

            self.client.publish(MQTT_TOPIC_CONTROLLER + "/timestamp", timestamp_json)

        except json.JSONDecodeError:
            logger.error("Error decoding JSON in MQTT payload")

    def report_error(self, error_message):
        logger.error(error_message)
        self.client.publish(MQTT_TOPIC_STATUS, error_message)
