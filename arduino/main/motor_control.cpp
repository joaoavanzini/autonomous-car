#include "motor_control.h"
#include <Arduino.h>

MotorControl::MotorControl(int enPin, int in1Pin, int in2Pin)
        : enPin(enPin), in1Pin(in1Pin), in2Pin(in2Pin), currentSpeed(0) {
}

void MotorControl::begin() {
    pinMode(enPin, OUTPUT);
    pinMode(in1Pin, OUTPUT);
    pinMode(in2Pin, OUTPUT);
}

void MotorControl::setSpeed(int speed) {
    currentSpeed = speed;
    analogWrite(enPin, speed);
}

int MotorControl::getSpeed() {
    return currentSpeed;
}

void MotorControl::moveForward() {
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
}

void MotorControl::moveBackward() {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
}

void MotorControl::stop() {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, LOW);
}
