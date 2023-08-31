#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

class MotorControl {
public:
    MotorControl(int enAPin, int enBPin, int in1Pin, int in2Pin, int in3Pin, int in4Pin);
    void begin();
    void setSpeed(int speed);
    int getSpeed();
    void moveForward();
    void moveBackward();
    void moveRight();
    void moveLeft();
    void stop();

private:
    int enAPin;
    int enBPin;
    int in1Pin;
    int in2Pin;
    int in3Pin;
    int in4Pin;
    int currentSpeed;
};

#endif
