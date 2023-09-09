# ultrasonic_sensor_data_reader.py
import serial
import json
from config import MQTT_BROKER_HOST, MQTT_DATA_ULTRASONIC_TOPIC, mqtt_client

def read_ultrasonic_data():
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
                        
                        # Enviar os dados do sensor em um evento
                        ultrasonic_event = {
                            "event": "ultrasonic_data",
                            "data": json_data
                        }
                        mqtt_client.publish(MQTT_DATA_ULTRASONIC_TOPIC, json.dumps(ultrasonic_event))
                    except Exception as e:
                        print(f"Error publishing ultrasonic data: {str(e)}")
                    buffer = b""
                elif buffer:
                    buffer += data

    except Exception as e:
        print(f"Error reading serial data: {str(e)}")
