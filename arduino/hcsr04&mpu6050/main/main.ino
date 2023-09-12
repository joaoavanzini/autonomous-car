#include <ArduinoJson.h>
#include "UltrasonicSensor.h"
#include "MPUSensor.h"

UltrasonicSensor leftSensor(10, 11);      // Left sensor
UltrasonicSensor centralSensor(8, 9);     // Central sensor
UltrasonicSensor rightSensor(6, 7);       // Right sensor
MPUSensor mpuSensor;

void setup() {
  Serial.begin(9600);
  leftSensor.begin();
  centralSensor.begin();
  rightSensor.begin();
  mpuSensor.begin();
}

void loop() {
  DynamicJsonDocument ultrasonicJson(200);
  DynamicJsonDocument mpuJson(200);

  leftSensor.update();
  centralSensor.update();
  rightSensor.update();
  mpuSensor.update();

  ultrasonicJson["left"] = leftSensor.getDistance();
  ultrasonicJson["central"] = centralSensor.getDistance();
  ultrasonicJson["right"] = rightSensor.getDistance();

  mpuJson["acceleration_x"] = mpuSensor.getAccelerationX();
  mpuJson["acceleration_y"] = mpuSensor.getAccelerationY();
  mpuJson["acceleration_z"] = mpuSensor.getAccelerationZ();
  mpuJson["gyro_x"] = mpuSensor.getGyroX();
  mpuJson["gyro_y"] = mpuSensor.getGyroY();
  mpuJson["gyro_z"] = mpuSensor.getGyroZ();
  mpuJson["temperature"] = mpuSensor.getTemperature();

  serializeJson(ultrasonicJson, Serial);
  Serial.println();
  serializeJson(mpuJson, Serial);
  Serial.println();
}
