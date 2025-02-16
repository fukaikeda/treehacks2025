#include "vibration_control.h"
#include <Arduino.h>

#define MOTOR1_PIN 6
#define MOTOR2_PIN 7
#define PELTIER_RELAY_PIN 8

void vibrationSetup() {
    pinMode(MOTOR1_PIN, OUTPUT);
    pinMode(MOTOR2_PIN, OUTPUT);
    pinMode(PELTIER_RELAY_PIN, OUTPUT);
}

void activateVibrationShort() {
    Serial.println("Vibration: Short mode");
    analogWrite(MOTOR1_PIN, 255);
    analogWrite(MOTOR2_PIN, 255);
    digitalWrite(PELTIER_RELAY_PIN, HIGH);
    delay(1000);
    analogWrite(MOTOR1_PIN, 0);
    analogWrite(MOTOR2_PIN, 0);
    digitalWrite(PELTIER_RELAY_PIN, LOW);
}

void activateVibrationLong() {
    Serial.println("Vibration: Long mode");
    digitalWrite(PELTIER_RELAY_PIN, HIGH);
    
    for (int i = 0; i <= 255; i += 5) {
        analogWrite(MOTOR1_PIN, i);
        analogWrite(MOTOR2_PIN, i);
        delay(50);
    }
    delay(2000);
    for (int i = 255; i >= 0; i -= 5) {
        analogWrite(MOTOR1_PIN, i);
        analogWrite(MOTOR2_PIN, i);
        delay(50);
    }
    digitalWrite(PELTIER_RELAY_PIN, LOW);
}

void stopVibration() {
    Serial.println("Stopping vibration...");
    analogWrite(MOTOR1_PIN, 0);
    analogWrite(MOTOR2_PIN, 0);
    digitalWrite(PELTIER_RELAY_PIN, LOW);
}
