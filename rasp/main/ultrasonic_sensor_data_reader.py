# ultrasonic_sensor_data_reader.py
import serial
import json
from config import MQTT_BROKER_HOST, MQTT_DATA_SENSORS_TOPIC
from mqtt_client import MQTTClient

def read_ultrasonic_data(mqtt_client):
    try:
        with serial.Serial("/dev/ttyACM0", baudrate=9600) as ser:
            print("Serial connection - open")

            buffer = b""

            while True:
                data = ser.read(1)
                if data == b'{':
                    buffer = b"{"
                elif buffer and data == b'\n':
                    try:
                        json_data = buffer.decode()
                        print(json_data)
                        mqtt_client.publish_ultrasonic_data(json_data)
                    except Exception as e:
                        print(f"Error publishing ultrasonic data: {str(e)}")
                    buffer = b""
                elif buffer:
                    buffer += data

    except Exception as e:
        print(f"Error reading serial data: {str(e)}")
