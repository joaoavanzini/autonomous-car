# motor.py
import RPi.GPIO as GPIO
from config import PWM_FREQUENCY

class Motor:
    def __init__(self, pwm_pin):
        self.pwm = GPIO.PWM(pwm_pin, PWM_FREQUENCY)
        self.pwm.start(0)

    def set_speed(self, speed):
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
