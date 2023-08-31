#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

class MotorControl {
public:
    MotorControl(int enPin, int in1Pin, int in2Pin);
    void begin();
    void setSpeed(int speed);
    int getSpeed();
    void moveForward();
    void moveBackward();
    void stop();

private:
    int enPin;
    int in1Pin;
    int in2Pin;
    int currentSpeed;
};

#endif
