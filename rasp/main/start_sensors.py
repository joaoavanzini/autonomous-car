# start_sensors.py

import serial
import json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER_HOST, MQTT_BROKER_PORT

# Tópico MQTT para o sensor MPU6050
MQTT_TOPIC_SENSOR_MPU6050 = "/rover/sensors/mpu6050"

# Tópico MQTT para o sensor HCSR05
MQTT_TOPIC_SENSOR_ULTRASONIC = "/rover/sensors/ultrasonic"

# Create an MQTT client instance
client = mqtt.Client("SensorDataReader")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection to MQTT broker failed")

# Set the MQTT client callbacks
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

try:
    with serial.Serial("/dev/ttyACM0", baudrate=9600) as ser:
        print("Serial connection - open")

        ultrasonic_buffer = b""
        mpu6050_buffer = b""
        
        while True:
            data = ser.read(1)
            if data == b'{':
                ultrasonic_buffer = b"{"
                mpu6050_buffer = b"{"
            elif ultrasonic_buffer and data == b'\n':
                try:
                    ultrasonic_json_data = ultrasonic_buffer.decode('utf-8', 'ignore')
                    ultrasonic_event = {
                        "event": "ultrasonic_data",
                        "data": ultrasonic_json_data.strip()
                    }
                    print(ultrasonic_event)
                    
                    # Publish the ultrasonic data to the MQTT topic
                    client.publish(MQTT_TOPIC_SENSOR_ULTRASONIC, json.dumps(ultrasonic_event))
                except Exception as e:
                    print(f"Error processing ultrasonic data: {str(e)}")
                ultrasonic_buffer = b""
            elif mpu6050_buffer and data == b'\n':
                try:
                    mpu6050_json_data = mpu6050_buffer.decode('utf-8', 'ignore')
                    mpu6050_event = {
                        "event": "mpu6050_data",
                        "data": mpu6050_json_data.strip()
                    }
                    print(mpu6050_event)
                    
                    # Publish the MPU6050 data to the MQTT topic
                    client.publish(MQTT_TOPIC_SENSOR_MPU6050, json.dumps(mpu6050_event))
                except Exception as e:
                    print(f"Error processing MPU6050 data: {str(e)}")
                mpu6050_buffer = b""
            elif ultrasonic_buffer:
                ultrasonic_buffer += data
            elif mpu6050_buffer:
                mpu6050_buffer += data

except Exception as e:
    print(f"Error reading serial data: {str(e)}")

# Start the MQTT client loop
client.loop_forever()
