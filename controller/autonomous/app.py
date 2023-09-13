import json
import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "192.168.0.105"
broker_port = 1883
ultrasonic_topic = "/rover/sensors/ultrasonic"
controller_topic = "/rover/controller"

# Create an MQTT client
client = mqtt.Client()

# Initialize rover state
rover_direction = "STOP"  # Default direction
min_distance = 50  # Minimum distance to react (in centimeters)

# Counter for consecutive left and right commands
consecutive_turn_count = 0
max_consecutive_turns = 5

# Callback when a message is received
def on_message(client, userdata, message):
    global rover_direction
    global consecutive_turn_count

    if message.topic == ultrasonic_topic:
        ultrasonic_data = json.loads(json.loads(message.payload.decode('utf-8'))['data'])
        
        # Check ultrasonic sensor data
        if ultrasonic_data["right"] < min_distance:
            rover_direction = "LEFT"
            consecutive_turn_count += 1
        elif ultrasonic_data["left"] < min_distance:
            rover_direction = "RIGHT"
            consecutive_turn_count += 1
        elif ultrasonic_data["central"] < min_distance:
            rover_direction = "BACKWARD"
            consecutive_turn_count = 0  # Reset the counter
        else:
            rover_direction = "FORWARD"
            consecutive_turn_count = 0  # Reset the counter

        # If consecutive turns exceed the threshold, go backward
        if consecutive_turn_count >= max_consecutive_turns:
            rover_direction = "BACKWARD"
            consecutive_turn_count = 0  # Reset the counter
        
        # Publish the new direction to control the rover
        controller_data = {
            "user_id": "auto",
            "direction": rover_direction,
            "speed": 35
        }
        client.publish(controller_topic, json.dumps(controller_data))
        print(f"New Rover Direction: {rover_direction}")

# Set the callback function for incoming messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Subscribe to the ultrasonic sensor topic
client.subscribe(ultrasonic_topic)

# Start the MQTT loop
client.loop_forever()
