// MPUSensor.h

#ifndef MPUSensor_h
#define MPUSensor_h

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

class MPUSensor {
public:
  MPUSensor();
  bool begin();
  void update();
  float getAccelerationX();
  float getAccelerationY();
  float getAccelerationZ();
  float getGyroX();
  float getGyroY();
  float getGyroZ();
  float getTemperature();

private:
  Adafruit_MPU6050 mpu;
};

#endif
