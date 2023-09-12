import json
import matplotlib.pyplot as plt

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
            
            # Remove ultrasonic values above 150 cm
            for key, value in ultrasonic_data.items():
                if value > 150:
                    ultrasonic_data[key] = 150
            
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
                print(f"Ignoring control message without 'speed' field: {line}")
    except json.JSONDecodeError:
        print(f"Ignoring invalid message: {line}")

# Create a figure with multiple subplots
fig, axes = plt.subplots(4, 1, figsize=(10, 12))

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

# Adjust subplot layout
plt.tight_layout()

# Show the figure with all subplots
plt.show()
