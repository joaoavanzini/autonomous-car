# config.py
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Pin configuration for motors
MOTOR1A_PIN = 7
MOTOR1B_PIN = 11
MOTOR1E_PIN = 22

MOTOR2A_PIN = 13
MOTOR2B_PIN = 16
MOTOR2E_PIN = 15

# PWM frequency
PWM_FREQUENCY = 100

# MQTT configuration
MQTT_BROKER_HOST = "192.168.0.104"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_CONTROLLER = "/controller"
MQTT_TOPIC_STATUS = "/status"

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR1A_PIN, GPIO.OUT)
GPIO.setup(MOTOR1B_PIN, GPIO.OUT)
GPIO.setup(MOTOR1E_PIN, GPIO.OUT)
GPIO.setup(MOTOR2A_PIN, GPIO.OUT)
GPIO.setup(MOTOR2B_PIN, GPIO.OUT)
GPIO.setup(MOTOR2E_PIN, GPIO.OUT)

# Create MQTT client
mqtt_client = mqtt.Client()
