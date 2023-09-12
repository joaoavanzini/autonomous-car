# rover.py
import RPi.GPIO as GPIO
from motor import Motor
from config import MOTOR1A_PIN, MOTOR1B_PIN, MOTOR1E_PIN, MOTOR2A_PIN, MOTOR2B_PIN, MOTOR2E_PIN, PWM_FREQUENCY
import paho.mqtt.publish as mqtt_publish

class Rover:
    def __init__(self):
        self.setup_gpio()
        self.setup_motors()

    def setup_gpio(self):
        # Clean up GPIO pins before setting up
        GPIO.cleanup()

        # Pin configuration for motors
        self.motor1a = MOTOR1A_PIN
        self.motor1b = MOTOR1B_PIN
        self.motor2a = MOTOR2A_PIN
        self.motor2b = MOTOR2B_PIN

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.motor1a, GPIO.OUT)
        GPIO.setup(self.motor1b, GPIO.OUT)
        GPIO.setup(self.motor2a, GPIO.OUT)
        GPIO.setup(self.motor2b, GPIO.OUT)

    def setup_motors(self):
        # Check if PWM objects already exist
        if not hasattr(self, 'motor1'):
            self.motor1 = Motor(MOTOR1E_PIN)
        if not hasattr(self, 'motor2'):
            self.motor2 = Motor(MOTOR2E_PIN)

    def move_forward(self, speed):
        try:
            self.motor1.set_speed(speed)
            self.motor2.set_speed(speed)
            GPIO.output(self.motor1a, GPIO.LOW)
            GPIO.output(self.motor1b, GPIO.HIGH)
            GPIO.output(self.motor2a, GPIO.LOW)
            GPIO.output(self.motor2b, GPIO.HIGH)
        except Exception as e:
            self.report_error(f"Error while moving backward: {str(e)}")

    def move_backward(self, speed):
        try:
            self.motor1.set_speed(speed)
            self.motor2.set_speed(speed)
            GPIO.output(self.motor1a, GPIO.HIGH)
            GPIO.output(self.motor1b, GPIO.LOW)
            GPIO.output(self.motor2a, GPIO.HIGH)
            GPIO.output(self.motor2b, GPIO.LOW)
        except Exception as e:
            self.report_error(f"Error while moving forward: {str(e)}")

    def turn_right(self, speed):
        try:
            self.motor1.set_speed(speed)
            self.motor2.set_speed(speed)
            GPIO.output(self.motor1a, GPIO.HIGH)
            GPIO.output(self.motor1b, GPIO.LOW)
            GPIO.output(self.motor2a, GPIO.LOW)
            GPIO.output(self.motor2b, GPIO.HIGH)
        except Exception as e:
            self.report_error(f"Error while turning right: {str(e)}")

    def turn_left(self, speed):
        try:
            self.motor1.set_speed(speed)
            self.motor2.set_speed(speed)
            GPIO.output(self.motor1a, GPIO.LOW)
            GPIO.output(self.motor1b, GPIO.HIGH)
            GPIO.output(self.motor2a, GPIO.HIGH)
            GPIO.output(self.motor2b, GPIO.LOW)
        except Exception as e:
            self.report_error(f"Error while turning left: {str(e)}")

    def stop(self, speed=None):
        try:
            self.motor1.stop()
            self.motor2.stop()
        except Exception as e:
            self.report_error(f"Error while stopping: {str(e)}")



    def cleanup_gpio(self):
        # Clean up GPIO pins after use
        GPIO.cleanup()

    def __del__(self):
        # Ensure GPIO cleanup when the object is deleted
        self.cleanup_gpio()

    def report_error(self, error_message):
        # Send the error message to the /status topic
        mqtt_publish.single(MQTT_TOPIC_STATUS, payload=error_message, hostname=MQTT_BROKER_HOST)