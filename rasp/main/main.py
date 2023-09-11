# main.py

import subprocess

# Start start_rover.py in the background
subprocess.Popen(["python3", "start_rover.py"])

# Start start_sensors.py in the background
subprocess.Popen(["python3", "start_sensors.py"])