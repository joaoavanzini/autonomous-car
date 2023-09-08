# ultrasonic_sensor_data_reader.py
import serial
import json
from config import MQTT_BROKER_HOST, MQTT_DATA_SENSORS_TOPIC
from mqtt_client import MQTTClient

def read_sensor_data(serial_port, mqtt_client):
    try:
        with serial.Serial(serial_port, baudrate=9600) as ser:
            print(f"Serial connection to {serial_port} - open")

            buffer = b""  # Inicialize um buffer vazio para armazenar os dados

            while True:
                data = ser.read(1)  # Leia um byte de cada vez
                if data == b'{':  # Se encontrar um '{', comece a coletar os dados
                    buffer = b"{"  # Inicialize o buffer com '{'
                elif buffer and data == b'\n':  # Se encontrar uma nova linha
                    try:
                        # Tente interpretar o buffer como JSON e, se bem-sucedido, publique-o
                        json_data = buffer.decode()
                        mqtt_client.publish_ultrasonic_data(json_data)
                    except Exception as e:
                        print(f"Error publishing ultrasonic data: {str(e)}")
                    buffer = b""  # Limpe o buffer
                elif buffer:  # Se o buffer estiver sendo preenchido, adicione os dados a ele
                    buffer += data

    except Exception as e:
        print(f"Error reading serial data: {str(e)}")
