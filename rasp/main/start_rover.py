# start_rover.py

from config import mqtt_client
from rover import Rover
from mqtt_client import MQTTClient

if __name__ == "__main__":
    rover = Rover()
    mqtt_client = MQTTClient()
    mqtt_client.connect()
    mqtt_client.subscribe()
    mqtt_client.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.client.disconnect()
        rover.cleanup_gpio()