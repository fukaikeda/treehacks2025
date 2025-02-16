#include "servo_control.h"
#include <Servo.h>
#include <Arduino.h>

Servo myservo;  
const int servoPin = 9;

void servoSetup() {
    myservo.attach(servoPin);
}

void moveServoShort() {
    for (int pos = 0; pos <= 180; pos += 1) {
        myservo.write(pos);
        delay(15);
    }
    for (int pos = 180; pos >= 0; pos -= 1) {
        myservo.write(pos);
        delay(15);
    }
}

void moveServoLong() {
    for (int pos = 0; pos <= 180; pos += 1) {
        myservo.write(pos);
        delay(10);
    }
    for (int pos = 180; pos >= 0; pos -= 1) {
        myservo.write(pos);
        delay(10);
    }
}
