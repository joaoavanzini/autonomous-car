import serial
import json
import paho.mqtt.client as mqtt

# MQTT Broker settings
MQTT_BROKER_HOST = "192.168.0.104"
MQTT_BROKER_PORT = 1883
MQTT_DATA_ULTRASONIC_TOPIC = "/rover/ultrasonic"

# Create an MQTT client instance
client = mqtt.Client("UltrasonicDataReader")

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
                    
                    # Publish the data to the MQTT topic
                    ultrasonic_event = {
                        "event": "ultrasonic_data",
                        "data": json_data
                    }
                    client.publish(MQTT_DATA_ULTRASONIC_TOPIC, json.dumps(ultrasonic_event))
                    print("Message published successfully.")
                except Exception as e:
                    print(f"Error processing ultrasonic data: {str(e)}")
                buffer = b""
            elif buffer:
                buffer += data

except Exception as e:
    print(f"Error reading serial data: {str(e)}")

# Start the MQTT client loop
client.loop_forever()
