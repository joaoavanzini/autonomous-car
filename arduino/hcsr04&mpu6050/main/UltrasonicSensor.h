// UltrasonicSensor.h

#ifndef UltrasonicSensor_h
#define UltrasonicSensor_h

#include <Arduino.h>

class UltrasonicSensor {
public:
  UltrasonicSensor(int trigPin, int echoPin);
  float measureDistance();

private:
  int trigPin;
  int echoPin;
};

#endif
