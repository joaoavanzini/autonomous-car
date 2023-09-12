#ifndef UltrasonicSensor_h
#define UltrasonicSensor_h

#include <Arduino.h>

class UltrasonicSensor {
public:
  UltrasonicSensor(int trigPin, int echoPin);
  void begin();
  void update();
  float getDistance();

private:
  int trigPin;
  int echoPin;
  unsigned long lastReadingTime;
  float lastDistance;
};

#endif
