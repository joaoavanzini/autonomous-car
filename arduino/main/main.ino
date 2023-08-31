#include "ultrassonic.h"
#include "motor_control.h"

//UltrasonicSensor ultrasonic1();
MotorControl motorControl(9, 4, 8, 7, 6, 5);

void setup() {
    //ultrasonic1.begin();
    motorControl.begin();

    motorControl.setSpeed(150);

    Serial.begin(9600);
}

void loop() {
//    unsigned int distance = ultrasonic1.getDistance();
//
//    if (distance > 0 && distance <= 10) {
//        motorControl.moveBackward();
//    } else {
//        motorControl.moveForward();
//    }
//
//    float speedMPS = pwmToMetersPerSecond(motorControl.getSpeed());  // Converte PWM em m/s
//    Serial.print("Velocidade (m/s): ");
//    Serial.println(speedMPS);
//
//    delay(100);

    motorControl.moveForward();
    delay(500);
    motorControl.stop();
    delay(1000);
    motorControl.moveBackward();
    delay(500);
    motorControl.stop();
    delay(1000);
    motorControl.moveRight();
    delay(200);
    motorControl.stop();
    delay(1000);
    motorControl.moveLeft();
    delay(200);
    motorControl.stop();
    delay(1000);

    //motorControl.stop();
}

// Função para converter PWM em velocidade em m/s
//float pwmToMetersPerSecond(int pwmValue) {
//    const int maxPWMValue = 255;
//    const float maxSpeed = 1.0;  // Velocidade máxima em m/s
//    return (float)pwmValue / maxPWMValue * maxSpeed;
//}

