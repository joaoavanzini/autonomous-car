// UltrasonicSensor.cpp

#include "UltrasonicSensor.h"

UltrasonicSensor::UltrasonicSensor(int trigPin, int echoPin) : trigPin(trigPin), echoPin(echoPin) {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

float UltrasonicSensor::measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  unsigned long duration = pulseIn(echoPin, HIGH);
  float distance = (duration * 0.0343) / 2;
  return distance;
}
