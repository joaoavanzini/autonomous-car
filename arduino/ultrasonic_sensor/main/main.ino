#include <ArduinoJson.h>
#include "UltrasonicSensor.h"

// Define the UltrasonicSensor instances
UltrasonicSensor leftSensor(10, 11);    // Left sensor
UltrasonicSensor centralSensor(8, 9);   // Central sensor
UltrasonicSensor rightSensor(6, 7);     // Right sensor

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Measure distances from all sensors
  float leftDistance = leftSensor.measureDistance();
  float centralDistance = centralSensor.measureDistance();
  float rightDistance = rightSensor.measureDistance();

  // Create a JSON object and send it via serial
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["left"] = leftDistance;
  jsonDoc["center"] = centralDistance;
  jsonDoc["right"] = rightDistance;

  serializeJson(jsonDoc, Serial);
  Serial.println(); // Add a new line at the end of JSON

}
