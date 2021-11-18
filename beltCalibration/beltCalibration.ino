#include <Servo.h>
#include <Stepper.h>
#include <Wire.h>

// Defining stepper motor info
const int stepsPerRevolution = 3200*4; // microstepping 1/16
const int dirPin = 12;
const int stepPin = 11;
int num_steps = 0;
int inKeyboard; //what user typed into serial
Stepper belt = Stepper(stepsPerRevolution, stepPin, dirPin);


void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  // setting speed of stepper motor for belt
  belt.setSpeed(50);
}

void loop() {
  // put your main code here, to run repeatedly:
   if (Serial.available()) {
    inKeyboard = Serial.read();
    switch (inKeyboard) { //determine appropiate function to run based on input
      case ' ': //continue looping
        belt.step(100);
        num_steps = num_steps + 100;
        Serial.print("We stepped "); Serial.print(num_steps); Serial.println(" times.");
        break;
      }
   }
}
