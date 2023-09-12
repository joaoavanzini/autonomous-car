import json
import matplotlib.pyplot as plt

# Initialize lists to store relevant data
controller_commands = []

# Initialize the initial coordinates of the rover
x_position = 0
y_position = 0

# Initialize lists to track the rover's path
x_positions = [x_position]
y_positions = [y_position]

# Read the "mqtt_messages.txt" file line by line
with open("mqtt_messages.txt", "r") as file:
    lines = file.readlines()

# Message processing
for line in lines:
    try:
        message_data = json.loads(line.split(", Message: ")[1])
        if "Topic: /rover/controller" in line:
            # Check if the "speed" field is present in the controller message
            if "speed" in message_data:
                controller_data = {
                    "user_id": message_data["user_id"],
                    "direction": message_data["direction"],
                    "speed": message_data["speed"],
                }
                controller_commands.append(controller_data)
    except json.JSONDecodeError:
        print(f"Ignoring invalid message: {line}")

# Process direction commands and update the rover's position on the map
for command in controller_commands:
    if command["direction"] == "FORWARD":
        # Calculate position change based on direction and speed
        delta_x = command["speed"]
        delta_y = 0
        x_position += delta_x
        y_position += delta_y
    elif command["direction"] == "BACKWARD":
        # Calculate position change based on direction and speed
        delta_x = -command["speed"]
        delta_y = 0
        x_position += delta_x
        y_position += delta_y
    elif command["direction"] == "LEFT":
        # Calculate position change based on direction and speed
        delta_x = 0
        delta_y = command["speed"]
        x_position += delta_x
        y_position += delta_y
    elif command["direction"] == "RIGHT":
        # Calculate position change based on direction and speed
        delta_x = 0
        delta_y = -command["speed"]
        x_position += delta_x
        y_position += delta_y

    # Record the new rover position in the path
    x_positions.append(x_position)
    y_positions.append(y_position)

# Create a map with a top-down view
plt.figure(figsize=(10, 10))

# Plot the rover's path
plt.plot(x_positions, y_positions, color='gray', alpha=0.7, label='Path')
plt.scatter(x_positions[0], y_positions[0], color='green', marker='o', s=100, label='Start')
plt.scatter(x_positions[-1], y_positions[-1], color='red', marker='o', s=100, label='End')

# Set the title and labels
plt.title("Rover Map Based on Position Data from Controller Commands")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.legend()

# Show the map
plt.grid(True)
plt.show()
