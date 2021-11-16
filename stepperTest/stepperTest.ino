#include <Stepper.h>

const int stepsPerRevolution = 3200*4; // microstepping 1/16
const int dirPin = 12;
const int stepPin = 11;

Stepper belt = Stepper(stepsPerRevolution, stepPin, dirPin);

void setup() {
  belt.setSpeed(100);
}

void loop() {
  belt.step(stepsPerRevolution);
  delay(2000);
  belt.step(-stepsPerRevolution);
  delay(2000);
}
