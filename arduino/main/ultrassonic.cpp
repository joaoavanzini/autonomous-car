#include "ultrassonic.h"
#include <Arduino.h>

UltrasonicSensor::UltrasonicSensor(int trigPin, int echoPin)
        : trigPin(trigPin), echoPin(echoPin), sonar(trigPin, echoPin, 200) {
}

void UltrasonicSensor::begin() {
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

unsigned int UltrasonicSensor::getDistance() {
    return sonar.ping_cm();
}

