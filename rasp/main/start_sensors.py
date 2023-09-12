import serial
import json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_TOPIC_SENSOR_ULTRASONIC, MQTT_TOPIC_SENSOR_MPU6050

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

        buffer = b""

        while True:
            data = ser.read(1)
            if data == b'{':
                buffer = b"{"
            elif buffer and data == b'\n':
                try:
                    json_data = buffer.decode('utf-8', 'ignore')
                    print(json_data)
                    
                    # Check if the JSON contains the "left" key to differentiate between sensor types
                    if "left" in json_data:
                        # Publish the data to the ultrasonic sensor topic
                        ultrasonic_event = {
                            "event": "ultrasonic_data",
                            "data": json_data
                        }
                        client.publish(MQTT_TOPIC_SENSOR_ULTRASONIC, json.dumps(ultrasonic_event))
                    else:
                        # Publish the data to the MPU6050 sensor topic
                        mpu6050_event = {
                            "event": "mpu6050_data",
                            "data": json_data
                        }
                        client.publish(MQTT_TOPIC_SENSOR_MPU6050, json.dumps(mpu6050_event))
                        
                except Exception as e:
                    print(f"Error processing sensor data: {str(e)}")
                buffer = b""
            elif buffer:
                buffer += data

except Exception as e:
    print(f"Error reading serial data: {str(e)}")

# Start the MQTT client loop
client.loop_forever()
