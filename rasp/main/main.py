# main.py
from config import mqtt_client
from rover import Rover
import multiprocessing
from ultrasonic_sensor_data_reader import UltrasonicDataReaderProcess
from config import MQTT_BROKER_HOST, MQTT_CONTROLLER_TOPIC

def main():
    rover = Rover()
    mqtt_client.connect(host=MQTT_BROKER_HOST)
    mqtt_client.subscribe(topic=MQTT_CONTROLLER_TOPIC)
    mqtt_client.loop_start()

    ultrasonic_process = UltrasonicDataReaderProcess(mqtt_client)  # Passa mqtt_client como argumento
    ultrasonic_process.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.disconnect()
        rover.cleanup_gpio()
        ultrasonic_process.terminate()

if __name__ == "__main__":
    main()