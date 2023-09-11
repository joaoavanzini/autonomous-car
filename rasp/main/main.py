# main.py

import subprocess
import signal
import os

# Start start_rover.py in the background and store the process object
rover_process = subprocess.Popen(["python3", "start_rover.py"])

# Start start_sensors.py in the background and store the process object
sensors_process = subprocess.Popen(["python3", "start_sensors.py"])

try:
    # Wait for Ctrl+C signal
    signal.signal(signal.SIGINT, signal.default_int_handler)
    signal.pause()
except KeyboardInterrupt:
    # Handle Ctrl+C by terminating both processes
    if rover_process.poll() is None:
        rover_process.terminate()  # Terminate the rover process if it's running

    if sensors_process.poll() is None:
        sensors_process.terminate()  # Terminate the sensors process if it's running

    # Optionally, you can wait for the processes to finish gracefully
    rover_process.wait()
    sensors_process.wait()
