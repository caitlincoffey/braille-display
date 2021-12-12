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
const int dirPin = 8;
const int stepPin = 10;
int num_steps = 0;
int inKeyboard; //what user typed into serial
Stepper belt = Stepper(stepsPerRevolution, stepPin, dirPin);


void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  // setting speed of stepper motor for belt
  belt.setSpeed(20); // 10 original speed, 20 works tho
  // attaching servos
  cam1.attach(3);  // listens to pin 3, longest
  cam2.attach(5);  // listens to pin 5
  cam3.attach(6);  // listens to pin 6, shortest
  // hit left most pin, 30
//  cam1.write(120); // 80 , 40 left most
//  cam2.write(140);
//  cam3.write(140); //100 , 140 right most
//  cam1.write(80); // 80 , 40 left most
//  cam2.write(90);
  //cam3.write(90); //100 , 140 right most
  //NOTES
  //FLAT: cam1: 80, cam2: 90, cam3: 100
  makeCamsFlat();
//  delay(3000);
  //rightPinsUp();
//  delay(3000);
//  bothPinsUp();
//  delay(2000);
//  bothPinsUp2();
}

void makeCamsFlat() {
  cam1.write(72); //
  cam2.write(80); // was 90
  cam3.write(90); // was 100
}

void leftPinsUp() {
  //cam1.write(170); // WAS 25
  cam1.write(25);
  cam2.write(90 - 52);
  cam3.write(100 - 52); //100 , 140 right most
}

void bothPinsUp() {
  cam1.write(150);
  //cam2.write(180); // does not have a pos currently
  //cam3.write(180); // does not have a pos currently
  
  cam2.write(90-52);
  cam3.write(100-52);
}

void bothPinsUp2() {
  cam2.write(90+60);
  cam3.write(90+60);
}

void rightPinsUp() {
  cam1.write(70 + 60); // 80 , 40 left most
  cam2.write(90 + 60);
  cam3.write(90 + 60); //100 , 140 right most
}

void loop() {
  // put your main code here, to run repeatedly:
  //leftPinsUp();
  //rightPinsUp();
   if (Serial.available()) {
    inKeyboard = Serial.read();
    switch (inKeyboard) { //determine appropiate function to run based on input
      case ' ': //continue looping
        belt.step(-1100);
        num_steps = num_steps + 1100; // 1100 steps ? 
        Serial.print("We stepped "); Serial.print(num_steps); Serial.println(" times.");
        break;
      }
   }
}
