# ultrasonic_sensor_data_reader.py
import serial
import json
from config import MQTT_BROKER_HOST, MQTT_DATA_SENSORS_TOPIC
from mqtt_client import MQTTClient

def read_sensor_data(serial_port):
    try:
        ser = serial.Serial(serial_port, baudrate=9600)
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                try:
                    return (data)
                except json.JSONDecodeError:
                    print("Error decoding JSON data from Arduino")
    except Exception as e:
        print(f"Error reading serial data: {str(e)}")
