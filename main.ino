#include <Arduino.h>
#include "fsm.h"
#include "servo_control.h"
#include "vibration_control.h"

void setup() {
    Serial.begin(9600);
    while (!Serial);
    Serial.println("System initialized. Starting in IDLE state.");
    
    servoSetup();       // Initialize servo
    vibrationSetup();   // Initialize motors and Peltier
}

void loop() {
    handleFSM();  // Call FSM loop
}
