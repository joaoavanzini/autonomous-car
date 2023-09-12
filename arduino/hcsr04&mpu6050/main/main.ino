#include <ArduinoJson.h>
#include "UltrasonicSensor.h"
#include "MPUSensor.h"

UltrasonicSensor leftSensor(10, 11);      // Left sensor
UltrasonicSensor centralSensor(8, 9);     // Central sensor
UltrasonicSensor rightSensor(6, 7);       // Right sensor
MPUSensor mpuSensor;

void setup() {
  Serial.begin(9600);
  if (!mpuSensor.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
}

void loop() {
  DynamicJsonDocument jsonDoc(200);

  float leftDistance = leftSensor.measureDistance();
  float centralDistance = centralSensor.measureDistance();
  float rightDistance = rightSensor.measureDistance();

  JsonObject sensorData = jsonDoc.to<JsonObject>();
  sensorData["acceleration_x"] = mpuSensor.getAccelerationX();
  sensorData["acceleration_y"] = mpuSensor.getAccelerationY();
  sensorData["acceleration_z"] = mpuSensor.getAccelerationZ();
  sensorData["gyro_x"] = mpuSensor.getGyroX();
  sensorData["gyro_y"] = mpuSensor.getGyroY();
  sensorData["gyro_z"] = mpuSensor.getGyroZ();
  sensorData["temperature"] = mpuSensor.getTemperature();
  sensorData["left"] = leftDistance;
  sensorData["central"] = centralDistance;
  sensorData["right"] = rightDistance;

  serializeJson(jsonDoc, Serial);
  Serial.println();
}
