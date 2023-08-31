#ifndef ULTRASSONIC_H
#define ULTRASSONIC_H

#include <NewPing.h>

class UltrasonicSensor {
public:
    UltrasonicSensor(int trigPin, int echoPin);
    void begin();
    unsigned int getDistance();

private:
    int trigPin;
    int echoPin;
    NewPing sonar;
};

#endif

