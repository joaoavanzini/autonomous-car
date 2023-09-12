#include "MPUSensor.h"

MPUSensor::MPUSensor() : lastReadingTime(0) {}

void MPUSensor::begin() {
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  delay(100);
} 

void MPUSensor::update() {
  unsigned long currentTime = millis();

  if (currentTime - lastReadingTime >= 0.001) { // Realiza leitura a cada 100ms
    mpu.getEvent(&a, &g, &temp);
    lastReadingTime = currentTime;
  }
}

float MPUSensor::getAccelerationX() {
  return a.acceleration.x;
}

float MPUSensor::getAccelerationY() {
  return a.acceleration.y;
}

float MPUSensor::getAccelerationZ() {
  return a.acceleration.z;
}

float MPUSensor::getGyroX() {
  return g.gyro.x;
}

float MPUSensor::getGyroY() {
  return g.gyro.y;
}

float MPUSensor::getGyroZ() {
  return g.gyro.z;
}

float MPUSensor::getTemperature() {
  return temp.temperature;
}
