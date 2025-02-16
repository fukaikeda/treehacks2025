#include <Servo.h>

// Servo Configuration
Servo compressionServo;
const int SERVO_PIN = 9;
const int SERVO_CLOSE_POS = 160;  // Compression position (adjust as needed)
const int SERVO_OPEN_POS = 90;    // Open position for release

// Vibration Motor Configuration
const int MOTOR1_PIN = 6;
const int MOTOR2_PIN = 7;
const int PELTIER_RELAY_PIN = 8;  // Optional cooling relay

void setup() {
    Serial.begin(9600);

    // Initialize Servo
    compressionServo.attach(SERVO_PIN);
    compressionServo.write(SERVO_OPEN_POS);  // Start in open position

    // Initialize Vibration Motors & Peltier
    pinMode(MOTOR1_PIN, OUTPUT);
    pinMode(MOTOR2_PIN, OUTPUT);
    pinMode(PELTIER_RELAY_PIN, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {  // Check if input is available
        char input = Serial.read();

        if (input == 'a') {  // Trigger compression and vibration on 'a' input
            Serial.println("Compression and vibration activated!");

            // Move the servo to simulate compression
            compressionServo.write(SERVO_CLOSE_POS);
            delay(2000);  // Hold for 2 seconds

            // Activate vibration motors
            vibratePattern();

            // Release the servo after vibration
            compressionServo.write(SERVO_OPEN_POS);
            delay(2000);  // Hold for 2 seconds
        }
    }
}

// Vibration pattern function
void vibratePattern() {
    for (int i = 0; i <= 255; i += 5) {  // Gradually increase vibration intensity
        analogWrite(MOTOR1_PIN, i);
        analogWrite(MOTOR2_PIN, i);
        delay(50);
    }
    delay(500);  // Vibrate at max intensity for 0.5 seconds

    for (int i = 255; i >= 0; i -= 5) {  // Gradually decrease vibration intensity
        analogWrite(MOTOR1_PIN, i);
        analogWrite(MOTOR2_PIN, i);
        delay(50);
    }

    // Alternate motors to create a different vibration pattern
    for (int i = 0; i < 3; i++) {
        analogWrite(MOTOR1_PIN, 255);
        analogWrite(MOTOR2_PIN, 0);
        delay(500);
        analogWrite(MOTOR1_PIN, 0);
        analogWrite(MOTOR2_PIN, 255);
        delay(500);
    }

    // Turn off both motors
    analogWrite(MOTOR1_PIN, 0);
    analogWrite(MOTOR2_PIN, 0);
}
