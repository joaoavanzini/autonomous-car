# main.py
from config import mqtt_client
from rover import Rover
from mqtt_client import MQTTClient
import multiprocessing
from ultrasonic_sensor_data_reader import read_sensor_data


def main():
    rover = Rover()
    mqtt_client = MQTTClient()
    mqtt_client.connect()
    mqtt_client.subscribe()
    mqtt_client.start()

    ultrasonic_process = multiprocessing.Process(target=read_ultrasonic_data, args=(mqtt_client,))
    ultrasonic_process.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.client.disconnect()
        rover.cleanup_gpio()
        ultrasonic_process.terminate()


def read_ultrasonic_data(mqtt_client):
    while True:
        ultrasonic_data = read_sensor_data("/dev/ttyACM0")
        if ultrasonic_data is not None:
            mqtt_client.publish_ultrasonic_data(ultrasonic_data)

if __name__ == "__main__":
    main()