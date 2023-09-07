# motor.py
import RPi.GPIO as GPIO
from config import PWM_FREQUENCY

class Motor:
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin
        self.pwm = None
        self.setup_pwm()

    def setup_pwm(self):
        # Clean up any existing PWM object for the GPIO channel
        if self.pwm is not None:
            self.pwm.stop()
            self.pwm = None

        # Set up the GPIO channel as an output
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        # Create a new PWM object
        self.pwm = GPIO.PWM(self.pwm_pin, PWM_FREQUENCY)
        self.pwm.start(0)

    def set_speed(self, speed):
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
