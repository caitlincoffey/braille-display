// Preliminary Arduino Driver file for Refreshable Braille Display
// Made for Sprint 3
#include <Servo.h>
#include <Stepper.h>
#include <Wire.h>

// Braille 1 or 2 switch
const int switchPin = A0;
int switchBraille1 = 0;
bool braille1 = true;

// Defining servos
Servo cam1;
Servo cam2;
Servo cam3;

// Defining stepper motor info
const int stepsPerRevolution = 3200*4; // microstepping 1/16
const int dirPin = 12;
const int stepPin = 11;
const int stepsToCell = 1100; //TODO determine actual value using beltCalibration program, stepsToCell == n
Stepper belt = Stepper(stepsPerRevolution, stepPin, dirPin);

//Defining cam positions
int A = 90; //0 0, 165 is start (right most) and 120 is end (left most)
int B = 180; //1 1
int C = 175; //0 1
int D = 110; //1 0

//defining for 2-way communication
const byte numChars = 64;
char receivedChars[numChars];
boolean newData = false;
bool started = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  // attaching servos
  cam1.attach(3);  // listens to pin 9
  cam2.attach(5);  // listens to pin 10
  cam3.attach(6);  // listens to pin 11

  // setting speed of stepper motor for belt
  belt.setSpeed(20); //could be 10 for safety
}

void loop() {
  recvWithStartEndMarkers(); //receive next character from Python
  if (receivedChars[0] == 'g' && receivedChars[1] == 'r' && receivedChars[2] == 'a' && receivedChars[3] == 'd' && receivedChars[4] == 'e' && started == false) { //send braille 1 or braille 2 python
    braille1 = gradeOfBraille();
    sendGradeToPython(braille1);
    delay(500);
    Serial.println("1");
    // Only send this code during start
    started = true;
  }
  else if (started == true and newData == true) {
    moveServos();
    delay(2000); // Arbirtrary pause for cams, anything greater than 3 sec is overkill
    replyToPython();
    belt.step(stepsToCell); //move to next cell
  }
}

void moveServos() {
  //move the servos to position for cells
  switch (receivedChars[0]) {
    case 'A':
      cam1.write(145);
      break;
    case 'B':
      cam1.write(180);
      break;
    case 'C':
      cam1.write(175);
      break;
    case 'D':
      cam1.write(110);
  }

  switch (receivedChars[1]) {
    case 'A':
      cam2.write(145);
      break;
    case 'B':
      cam2.write(180);
      break;
    case 'C':
      cam2.write(175);
      break;
    case 'D':
      cam2.write(110);
  }

  switch (receivedChars[2]) {
    case 'A':
      cam3.write(145);
      break;
    case 'B':
      cam3.write(180);
      break;
    case 'C':
      cam3.write(175);
      break;
    case 'D':
      cam3.write(110);
  }
}

//following adapted from: https://forum.arduino.cc/t/pc-arduino-comms-using-python-updated/574496
void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ind = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ind] = rc;
        //Serial.println(receivedChars[ind]);
        ind++;
        if (ind >= numChars) {
          ind = numChars - 1;
        }
      }
      else {
        receivedChars[ind] = '\0'; //terminate the string
        recvInProgress = false;
        ind = 0;
        newData = true;
      }
    }
    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

void replyToPython() {
  if (newData == true) {
    Serial.println("1");
    newData = false;
  }
}

bool gradeOfBraille() {
  // Braille 1 vs. Braille 2
  switchBraille1 = digitalRead(switchPin);
  if (switchBraille1 == LOW) {
    braille1 = true;
  }
  else if (switchBraille1 == HIGH) {
    braille1 = false; // braille 2
  }
 return braille1;
}

void sendGradeToPython(bool braille1) {
  // Checks grade and sends data to Python
  if (braille1 == true) {
    Serial.println(2);
  }
  if (braille1 == false) {
    Serial.println(3);
  }
}
