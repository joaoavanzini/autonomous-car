# main.py
from config import mqtt_client
from rover import Rover
import multiprocessing
from ultrasonic_sensor_data_reader import read_ultrasonic_data
from config import mqtt_client, MQTT_BROKER_HOST

def main():
    rover = Rover()
    mqtt_client.connect(host=MQTT_BROKER_HOST)
    mqtt_client.subscribe()
    mqtt_client.start()

    ultrasonic_process = multiprocessing.Process(target=read_ultrasonic_data)
    ultrasonic_process.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.client.disconnect()
        rover.cleanup_gpio()
        ultrasonic_process.terminate()

if __name__ == "__main__":
    main()