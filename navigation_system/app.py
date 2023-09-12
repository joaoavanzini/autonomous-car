import paho.mqtt.client as mqtt
import time

# MQTT broker settings
broker_address = "192.168.0.105"  # Change this to your MQTT broker's address
broker_port = 1883  # Change this to your MQTT broker's port

# Text file to store MQTT messages
output_file = "mqtt_messages.txt"

# Callback when a message is received
def on_message(client, userdata, message):
    with open(output_file, "a") as file:
        file.write(f"Topic: {message.topic}, Message: {message.payload.decode('utf-8')}\n")

# Create an MQTT client
client = mqtt.Client()

# Set the callback function for incoming messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Subscribe to all topics (you can change the topic to a specific one if needed)
client.subscribe("#")

# Start the MQTT loop
client.loop_start()

try:
    while True:
        # You can add other code here if needed
        time.sleep(1)
except KeyboardInterrupt:
    # Disconnect from the MQTT broker and stop the loop when the script is interrupted
    client.disconnect()
    client.loop_stop()
