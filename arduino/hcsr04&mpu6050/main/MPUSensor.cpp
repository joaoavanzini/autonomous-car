// MPUSensor.cpp

#include "MPUSensor.h"

MPUSensor::MPUSensor() {}

bool MPUSensor::begin() {
  if (!mpu.begin()) {
    return false;
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  delay(100);
  return true;
}

void MPUSensor::update() {
  // Não é necessário atualizar, já que os valores serão lidos diretamente na função get.
}

float MPUSensor::getAccelerationX() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return a.acceleration.x;
}

float MPUSensor::getAccelerationY() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return a.acceleration.y;
}

float MPUSensor::getAccelerationZ() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return a.acceleration.z;
}

float MPUSensor::getGyroX() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return g.gyro.x;
}

float MPUSensor::getGyroY() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return g.gyro.y;
}

float MPUSensor::getGyroZ() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return g.gyro.z;
}

float MPUSensor::getTemperature() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return temp.temperature;
}
