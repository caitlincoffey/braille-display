#include <Servo.h>
#include <Stepper.h>
#include <Wire.h>
#include <Servo.h>

// Defining servos
Servo cam1;
Servo cam2;
Servo cam3;

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
  belt.setSpeed(20); // 10 original speed, 20 works tho
  // attaching servos
  cam1.attach(3);  // listens to pin 3
  cam2.attach(5);  // listens to pin 5
  cam3.attach(6);  // listens to pin 6
  // hit left most pin, 30
  cam1.write(40); // 80 , 40 left most
  cam2.write(0);
  cam3.write(140); //100 , 140 right most
}

void loop() {
  // put your main code here, to run repeatedly:

   if (Serial.available()) {
    inKeyboard = Serial.read();
    switch (inKeyboard) { //determine appropiate function to run based on input
      case ' ': //continue looping
        belt.step(1100);
        num_steps = num_steps + 1100; // 1100 steps ? 
        Serial.print("We stepped "); Serial.print(num_steps); Serial.println(" times.");
        break;
      }
   }
}
