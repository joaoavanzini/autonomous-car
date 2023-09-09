# motor.py
import RPi.GPIO as GPIO
from config import PWM_FREQUENCY

class Motor:
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin
        self.pwm = None

    def setup_pwm(self):
        # Check if a PWM object already exists for this GPIO channel
        if self.pwm is None:
            # Set up the GPIO channel as an output
            GPIO.setup(self.pwm_pin, GPIO.OUT)
            # Create a new PWM object
            self.pwm = GPIO.PWM(self.pwm_pin, PWM_FREQUENCY)
            self.pwm.start(0)

    def cleanup_pwm(self):
        # Clean up the existing PWM object
        if self.pwm is not None:
            self.pwm.stop()
            self.pwm = None

    def set_speed(self, speed):
        self.setup_pwm()  # Ensure PWM setup before changing speed
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        self.setup_pwm()  # Ensure PWM setup before stopping
        self.pwm.ChangeDutyCycle(0)