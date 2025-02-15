enum State {
    IDLE,
    COMPRESS,
    RELEASE
};

State currentState = IDLE;  // Start in IDLE state

void setup() {
    Serial.begin(9600);
    while (!Serial);
    Serial.println("System initialized. Starting in IDLE state.");
}

void loop() {
    switch (currentState) {
        case IDLE:
            Serial.println("State: IDLE. Waiting for input to start compression...");
            if (Serial.available() > 0) {  // Simulating an event trigger
                char input = Serial.read();
                if (input == 's') {  // 's' for start compression
                    Serial.println("Starting compression...");
                    currentState = COMPRESS;
                }
            }
            delay(500);
            break;

        case COMPRESS:
            Serial.println("State: COMPRESS. Performing compression...");
            delay(2000);  // Simulate compression duration
            Serial.println("Compression done. Moving to RELEASE state.");
            currentState = RELEASE;
            break;

        case RELEASE:
            Serial.println("State: RELEASE. Releasing...");
            delay(1500);  // Simulate release duration
            Serial.println("Release complete. Returning to IDLE.");
            currentState = IDLE;
            break;
    }
}
