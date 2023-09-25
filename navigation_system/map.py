import json
import matplotlib.pyplot as plt
import numpy as np

# Rover properties
rover_weight = 1280  # grams

# Initialize lists to store relevant data
ultrasonic_data_list = []
mpu6050_data_list = []
controller_commands = []

# Initialize lists to store direction moments
left_directions = []
right_directions = []
forward_directions = []
backward_directions = []
stop_directions = []

# Rover initial state
x_position = 0
y_position = 0
orientation = 0
linear_velocity = 0
angular_velocity = 0

# Lists to store kinematic data
timestamps = []  # Timestamps for the data points
positions = []  # Rover positions
velocities = []  # Rover linear velocities
orientations = []  # Rover orientations

# Time step (you might need to adjust this based on your data)
time_step = 0.1  # seconds

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
                "left": min(data["left"], 150),  # Limit max distance to 150 cm
                "central": min(data["central"], 150),
                "right": min(data["right"], 150),
            }
            ultrasonic_data_list.append(ultrasonic_data)
        elif "Topic: /rover/sensors/mpu6050" in line:
            # Load additional JSON data from the MPU6050 message
            data = json.loads(message_data["data"])
            mpu6050_data = {
                "acceleration_x": data["acceleration_x"],
                "acceleration_y": data["acceleration_y"],
                "gyro_x": data["gyro_x"],
                "gyro_y": data["gyro_y"],
                "gyro_z": data["gyro_z"],
            }
            mpu6050_data_list.append(mpu6050_data)
        elif "Topic: /rover/controller" in line:
            # Check if the "speed" field is present in the controller message
            if "speed" in message_data:
                controller_data = {
                    "user_id": message_data["user_id"],
                    "direction": message_data["direction"],
                    "speed": message_data["speed"],
                }
                controller_commands.append(controller_data)

                # Identify direction moments
                if message_data["direction"] == "RIGHT":
                    right_directions.append(len(ultrasonic_data_list))
                elif message_data["direction"] == "LEFT":
                    left_directions.append(len(ultrasonic_data_list))
                elif message_data["direction"] == "FORWARD":
                    forward_directions.append(len(ultrasonic_data_list))
                elif message_data["direction"] == "BACKWARD":
                    backward_directions.append(len(ultrasonic_data_list))
                elif message_data["direction"] == "STOP":
                    stop_directions.append(len(ultrasonic_data_list))
            else:
                # Handle control messages without "speed" field by ignoring them
                print(f"Ignoring control message without 'speed' field: {line}")
    except json.JSONDecodeError:
        # Handle invalid messages by ignoring them
        print(f"Ignoring invalid message: {line}")

# Kinematics calculations and data recording
for i in range(1, len(mpu6050_data_list)):
    # Calculate linear acceleration
    acceleration_x = mpu6050_data_list[i]["acceleration_x"]
    acceleration_y = mpu6050_data_list[i]["acceleration_y"]
    linear_acceleration = np.sqrt(acceleration_x**2 + acceleration_y**2)
    
    # Calculate angular acceleration
    gyro_z = mpu6050_data_list[i]["gyro_z"]
    angular_acceleration = gyro_z
    
    # Update velocities
    linear_velocity += linear_acceleration * time_step
    angular_velocity += angular_acceleration * time_step
    
    # Update positions
    orientation += angular_velocity * time_step
    x_position += linear_velocity * np.cos(orientation) * time_step
    y_position += linear_velocity * np.sin(orientation) * time_step
    
    # Record kinematic data
    timestamps.append(i * time_step)
    positions.append((x_position, y_position))
    velocities.append(linear_velocity)
    orientations.append(orientation)

# Calculate total distance traveled
total_distance = 0

# Initialize variables to track the previous position
prev_x = positions[forward_directions[0]][0]
prev_y = positions[forward_directions[0]][1]

# Iterate over the indices of "FORWARD" direction
for index in forward_directions:
    x, y = positions[index]  # Current position
    distance = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)  # Distance between positions
    total_distance += distance  # Add to total distance
    prev_x, prev_y = x, y  # Update previous position

# Convert the total distance from meters to centimeters
total_distance_cm = total_distance * 100

print(f"Total distance traveled: {total_distance_cm:.2f} cm")

# Create a figure with multiple subplots
fig, axes = plt.subplots(7, 1, figsize=(10, 18))

# Plot ultrasonic sensor data
axes[0].plot([data["left"] for data in ultrasonic_data_list], label="Left Distance")
axes[0].plot([data["central"] for data in ultrasonic_data_list], label="Central Distance")
axes[0].plot([data["right"] for data in ultrasonic_data_list], label="Right Distance")
axes[0].set_xlabel("Time Steps")
axes[0].set_ylabel("Distance (cm)")
axes[0].set_title("Rover Ultrasonic Sensor Data")
axes[0].legend()
axes[0].grid(True)

# Plot MPU6050 data - Acceleration
axes[1].plot([data["acceleration_x"] for data in mpu6050_data_list], label="Acceleration X")
axes[1].plot([data["acceleration_y"] for data in mpu6050_data_list], label="Acceleration Y")
axes[1].set_xlabel("Time Steps")
axes[1].set_ylabel("Acceleration (m/s^2)")
axes[1].set_title("Rover MPU6050 Acceleration Data")
axes[1].legend()
axes[1].grid(True)

# Plot MPU6050 data - Gyro
axes[2].plot([data["gyro_x"] for data in mpu6050_data_list], label="Gyro X")
axes[2].plot([data["gyro_y"] for data in mpu6050_data_list], label="Gyro Y")
axes[2].plot([data["gyro_z"] for data in mpu6050_data_list], label="Gyro Z")
axes[2].set_xlabel("Time Steps")
axes[2].set_ylabel("Angular Velocity (rad/s)")
axes[2].set_title("Rover MPU6050 Gyro Data")
axes[2].legend()
axes[2].grid(True)

# Plot direction moments
axes[3].plot(left_directions, [1] * len(left_directions), 'ro', label="Left Direction")
axes[3].plot(right_directions, [1] * len(right_directions), 'bo', label="Right Direction")
axes[3].plot(forward_directions, [1] * len(forward_directions), 'go', label="Forward Direction")
axes[3].plot(backward_directions, [1] * len(backward_directions), 'mo', label="Backward Direction")
axes[3].plot(stop_directions, [1] * len(stop_directions), 'ko', label="Stop")
axes[3].set_xlabel("Time Steps")
axes[3].set_title("Rover Direction Commands")
axes[3].legend()
axes[3].grid(True)

# Plot rover position
x_positions = [pos[0] for pos in positions]
y_positions = [pos[1] for pos in positions]
axes[4].plot(x_positions, y_positions, label="Rover Position")
axes[4].set_xlabel("X Position (m)")
axes[4].set_ylabel("Y Position (m)")
axes[4].set_title("Rover Position")
axes[4].legend()
axes[4].grid(True)

# Plot linear velocity
axes[5].plot(timestamps, velocities, label="Linear Velocity")
axes[5].set_xlabel("Time Steps")
axes[5].set_ylabel("Linear Velocity (m/s)")
axes[5].set_title("Rover Linear Velocity")
axes[5].legend()
axes[5].grid(True)

# Plot orientation
axes[6].plot(timestamps, orientations, label="Orientation")
axes[6].set_xlabel("Time Steps")
axes[6].set_ylabel("Orientation (rad)")
axes[6].set_title("Rover Orientation")
axes[6].legend()
axes[6].grid(True)

# Adjust subplot layout
plt.tight_layout()

# Show the figure with all subplots
plt.show()
