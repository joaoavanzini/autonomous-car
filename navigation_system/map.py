import json
import matplotlib.pyplot as plt
import numpy as np

# Initialize lists to store relevant data
ultrasonic_data_list = []
controller_commands = []

# Initialize the initial coordinates of the rover and orientation
x_position = 0
y_position = 0
orientation = 90  # Angle in degrees (90 degrees represents upward direction)

# Initialize lists to track the rover's path
x_positions = [x_position]
y_positions = [y_position]

# Initialize variables to track gyro angle
gyro_angle_x = 0  # Initial angle around the X-axis
gyro_angle_y = 0  # Initial angle around the Y-axis

# Read the "mqtt_messages.txt" file line by line
with open("mqtt_messages.txt", "r") as file:
    lines = file.readlines()

# Message processing
for line in lines:
    try:
        message_data = json.loads(line.split(", Message: ")[1])
        if "Topic: /rover/sensors/ultrasonic" in line:
            # Load additional JSON data from the ultrasonic message
            data = json.loads(message_data["data"])
            ultrasonic_data = {
                "left": data["left"],
                "central": data["central"],
                "right": data["right"],
            }
            ultrasonic_data_list.append(ultrasonic_data)
        elif "Topic: /rover/controller" in line:
            # Check if the "speed" field is present in the controller message
            if "speed" in message_data:
                controller_data = {
                    "user_id": message_data["user_id"],
                    "direction": message_data["direction"],
                    "speed": message_data["speed"],
                }
                controller_commands.append(controller_data)
        elif "Topic: /rover/sensors/mpu6050" in line:
            # Load additional JSON data from the MPU6050 (gyro) message
            data = json.loads(message_data["data"])
            gyro_x = data["gyro_x"]
            gyro_y = data["gyro_y"]

            # Update gyro angles around the X and Y axes
            gyro_angle_x += gyro_x
            gyro_angle_y += gyro_y

    except json.JSONDecodeError:
        print(f"Ignoring invalid message: {line}")

# Create a map with a top-down view
plt.figure(figsize=(10, 10))

# Process direction commands and update the rover's position on the map
for command in controller_commands:
    if command["direction"] == "RIGHT":
        orientation -= 90
    elif command["direction"] == "LEFT":
        orientation += 90
    elif command["direction"] == "FORWARD":
        # Use rover orientation to calculate position change
        delta_x = command["speed"] * np.cos(np.radians(orientation))
        delta_y = command["speed"] * np.sin(np.radians(orientation))
        
        # Check ultrasonic data before moving
        if ultrasonic_data_list:
            central_ultrasonic = ultrasonic_data_list[-1]["central"]
            if central_ultrasonic < 10:  # If central distance is less than 10 cm, stop
                command["speed"] = 0
        
        x_position += delta_x
        y_position += delta_y
    elif command["direction"] == "BACKWARD":
        # Use rover orientation to calculate position change
        delta_x = -command["speed"] * np.cos(np.radians(orientation))
        delta_y = -command["speed"] * np.sin(np.radians(orientation))
        x_position += delta_x
        y_position += delta_y

    # Use gyro angles around the X and Y axes to adjust orientation
    orientation += gyro_angle_x
    orientation += gyro_angle_y

    # Record the new rover position in the path
    x_positions.append(x_position)
    y_positions.append(y_position)

# Plot the rover's path
plt.plot(x_positions, y_positions, color='gray', alpha=0.7, label='Path')
plt.scatter(x_positions[0], y_positions[0], color='green', marker='o', s=100, label='Start')
plt.scatter(x_positions[-1], y_positions[-1], color='red', marker='o', s=100, label='End')

# Set the title and labels
plt.title("Rover Map with Gyro Data (X and Y Axes) and Obstacle Avoidance Using Ultrasonic")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.legend()

# Show the map
plt.grid(True)
plt.show()
