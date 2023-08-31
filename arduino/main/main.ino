#include "ultrassonic.h"
#include "motor_control.h"
#include <ArduinoJson.h>

UltrasonicSensor ultrasonicRight(10, 11);
UltrasonicSensor ultrasonicCenter(2, 3);
UltrasonicSensor ultrasonicLeft(12, 13);
MotorControl motorControl(9, 4, 8, 7, 6, 5);

void setup() {
    ultrasonicRight.begin();
    ultrasonicCenter.begin();
    ultrasonicLeft.begin();

    motorControl.begin();
    motorControl.setSpeed(150);

    Serial.begin(115200);
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        executeCommand(command);
    }

    // Criar um objeto JSON para os dados dos sensores
    StaticJsonDocument<256> jsonDoc;
    jsonDoc["right"] = ultrasonicRight.getDistance();
    jsonDoc["center"] = ultrasonicCenter.getDistance();
    jsonDoc["left"] = ultrasonicLeft.getDistance();

    // Serializar o objeto JSON e enviá-lo
    String jsonData;
    serializeJson(jsonDoc, jsonData);
    Serial.println(jsonData);

    delay(10);  // Aguardar um 1 decimo de segundo
}

void executeCommand(char cmd) {
    switch (cmd) {
        case 'w':
            motorControl.moveForward();
            break;
        case 'a':
            motorControl.moveLeft();
            break;
        case 'd':
            motorControl.moveRight();
            break;
        case 's':
            motorControl.moveBackward();
            break;
        default:
            motorControl.stop();
    }
}
