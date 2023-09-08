# ultrasonic_sensor_data_reader.py
import serial
import json
from config import MQTT_BROKER_HOST, MQTT_DATA_SENSORS_TOPIC

def read_and_publish_sensor_data(serial_port, mqtt_client):
    try:
        ser = serial.Serial(serial_port, baudrate=9600)  # Modify the baudrate as needed
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                try:
                    sensor_data = json.loads(data)
                    mqtt_client.publish(MQTT_DATA_SENSORS_TOPIC, json.dumps(sensor_data))
                except json.JSONDecodeError:
                    print("Error decoding JSON data from Arduino")
    except Exception as e:
        print(f"Error reading serial data: {str(e)}")
