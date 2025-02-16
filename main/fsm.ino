#include "fsm.h"
#include "servo_control.h"
#include <Arduino.h>

State currentState = IDLE;  // Start in IDLE state

void handleFSM() {
    switch (currentState) {
        case IDLE:
            Serial.println("State: IDLE. Waiting for input to start compression...");
            if (Serial.available() > 0) {
                char input = Serial.read();
                if (input == 's') {
                    Serial.println("Starting SHORT compression...");
                    currentState = SHORT;
                } else if (input == 'l') {
                    Serial.println("Starting LONG compression...");
                    currentState = LONG;
                }
            }
            delay(500);
            break;

        case SHORT:
            Serial.println("State: SHORT. Performing short compression...");
            moveServoShort();  // Call function from servo_control.cpp
            Serial.println("Short compression done. Moving to RELEASE state.");
            currentState = RELEASE;
            break;

        case LONG:
            Serial.println("State: LONG. Performing long compression...");
            moveServoLong();  // Call function from servo_control.cpp
            Serial.println("Long compression done. Moving to RELEASE state.");
            currentState = RELEASE;
            break;

        case RELEASE:
            Serial.println("State: RELEASE. Releasing...");
            delay(1500);
            Serial.println("Release complete. Returning to IDLE.");
            currentState = IDLE;
            break;
    }
}
