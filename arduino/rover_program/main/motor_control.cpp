#include "motor_control.h"
#include <Arduino.h>

MotorControl::MotorControl(int enAPin, int enBPin, int in1Pin, int in2Pin, int in3Pin, int in4Pin)
        : enAPin(enAPin), enBPin(enBPin), in1Pin(in1Pin), in2Pin(in2Pin), in3Pin(in3Pin), in4Pin(in4Pin), currentSpeed(0) {
}

void MotorControl::begin() {
    pinMode(enAPin, OUTPUT);
    pinMode(enBPin, OUTPUT);
    pinMode(in1Pin, OUTPUT);
    pinMode(in2Pin, OUTPUT);
    pinMode(in3Pin, OUTPUT);
    pinMode(in4Pin, OUTPUT);
}

void MotorControl::setSpeed(int speed) {
    currentSpeed = speed;
    analogWrite(enAPin, speed);
    analogWrite(enBPin, speed);
}

int MotorControl::getSpeed() {
    return currentSpeed;
}

void MotorControl::moveForward() {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
    digitalWrite(in3Pin, HIGH);
    digitalWrite(in4Pin, LOW);
}

void MotorControl::moveBackward() {
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
    digitalWrite(in3Pin, LOW);
    digitalWrite(in4Pin, HIGH);
}

void MotorControl::moveRight() {
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
    digitalWrite(in3Pin, HIGH);
    digitalWrite(in4Pin, LOW);
}

void MotorControl::moveLeft() {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
    digitalWrite(in3Pin, LOW);
    digitalWrite(in4Pin, HIGH);
}

void MotorControl::stop() {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, LOW);
    digitalWrite(in3Pin, LOW);
    digitalWrite(in4Pin, LOW);
}
