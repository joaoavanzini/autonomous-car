# main.py
from config import mqtt_client
from rover import Rover
from mqtt_client import MQTTClient
import serial
import json
from ultrasonic_sensor_data_reader import read_and_publish_sensor_data


if __name__ == "__main__":
    rover = Rover()
    mqtt_client = MQTTClient()
    mqtt_client.connect()
    mqtt_client.subscribe()
    mqtt_client.start()

    read_and_publish_sensor_data("/dev/ttyUSB0", mqtt_client)  # Modify the serial port as needed

    try:
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.client.disconnect()
        rover.cleanup_gpio()
