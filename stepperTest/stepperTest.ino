#include <Wire.h>
#include <Adafruit_MotorShield.h>
//#include "Adafruit_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 2);
void setup() {
  // put your setup code here, to run once:
  myMotor ->setSpeed(200);

}

void loop() {
  // put your main code here, to run repeatedly:
  myMotor ->step(100, FORWARD, INTERLEAVE);

}

//#include <AFMotor.h>
//
//
//AF_Stepper motor(200, 2);
//
//
//void setup() {
//  Serial.begin(9600);           // set up Serial library at 9600 bps
//  Serial.println("Stepper test!");
//
//  motor.setSpeed(10);  // 10 rpm   
//
//  motor.step(100, FORWARD, SINGLE); 
//  motor.release();
//  delay(1000);
//}
//
//void loop() {
//  motor.step(100, FORWARD, SINGLE); 
//  motor.step(100, BACKWARD, SINGLE); 
//
//  motor.step(100, FORWARD, DOUBLE); 
//  motor.step(100, BACKWARD, DOUBLE);
//
//  motor.step(100, FORWARD, INTERLEAVE); 
//  motor.step(100, BACKWARD, INTERLEAVE); 
//
//  motor.step(100, FORWARD, MICROSTEP); 
//  motor.step(100, BACKWARD, MICROSTEP); 
//}
