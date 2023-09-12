#include "UltrasonicSensor.h"

UltrasonicSensor::UltrasonicSensor(int trigPin, int echoPin)
    : trigPin(trigPin), echoPin(echoPin), lastReadingTime(0), lastDistance(0) {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void UltrasonicSensor::begin() {
  // Inicialização do sensor, se necessário.
}

void UltrasonicSensor::update() {
  unsigned long currentTime = millis();

  if (currentTime - lastReadingTime >= 0.001) { // Realiza leitura a cada 100ms
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    unsigned long duration = pulseIn(echoPin, HIGH);
    lastDistance = (duration * 0.0343) / 2;
    lastReadingTime = currentTime;
  }
}

float UltrasonicSensor::getDistance() {
  return lastDistance;
}
