# mqtt_client.py
import paho.mqtt.client as mqtt
import json
import logging
from config import (
    MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_CONTROLLER_TOPIC, MQTT_STATUS_TOPIC, MQTT_DATA_SENSORS_TOPIC, MQTT_DATA_ULTRASONIC_TOPIC
)
from rover import Rover

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
        print("#8")

    def subscribe(self):
        self.client.subscribe(MQTT_CONTROLLER_TOPIC)
        print("#7")

    def start(self):
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        print("#6")
        payload = msg.payload.decode()
        try:
            data = json.loads(payload)
            direction = data.get('direction', 'STOP')
            speed = data.get('speed', 100)

            # Mapping directions to Rover class methods
            direction_map = {
                'FORWARD': self.rover.move_forward,
                'BACKWARD': self.rover.move_backward,
                'RIGHT': self.rover.turn_right,
                'LEFT': self.rover.turn_left,
                'STOP': self.rover.stop
            }

            # Execute the corresponding action
            action = direction_map.get(direction)
            if action:
                action(speed)
                # Enviar mensagem informativa para MQTT_STATUS_TOPIC
                status_message = {
                    "turning to": direction,
                    "speed": speed
                }
                self.client.publish(MQTT_STATUS_TOPIC, json.dumps(status_message))

                # Verifique se há um evento de ultrassom no payload e publique-o no tópico MQTT_DATA_ULTRASONIC_TOPIC
                if 'ultrasonic' in data:
                    ultrasonic_event = {
                        "event": "ultrasonic_data",
                        "data": data['ultrasonic']
                    }
                    print("#3")
                    self.client.publish(MQTT_DATA_ULTRASONIC_TOPIC, json.dumps(ultrasonic_event))
            else:
                error_message = f"Invalid direction: {direction}"
                logger.error(error_message)
                self.report_error(error_message)
        except json.JSONDecodeError:
            logger.error("Error decoding JSON in MQTT payload")


    def report_error(self, error_message):
        # Send the error message to the /status topic and log it
        logger.error(error_message)
        self.client.publish(MQTT_STATUS_TOPIC, error_message)

    def publish_ultrasonic_data(self, ultrasonic_data):
            print("#4")
            try:
                self.client.publish(MQTT_DATA_SENSORS_TOPIC, ultrasonic_data)
                print("#5")
            except Exception as e:
                logger.error(f"Error publishing ultrasonic data: {str(e)}")
