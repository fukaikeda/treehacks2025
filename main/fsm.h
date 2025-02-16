#ifndef FSM_H
#define FSM_H

enum State {
    IDLE,
    SHORT,
    LONG,
    RELEASE
};

extern State currentState;  // Global variable to track state

void handleFSM();  // Function to handle state transitions

#endif