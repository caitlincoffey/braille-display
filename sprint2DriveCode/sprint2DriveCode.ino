// Preliminary Arduino Driver file for Refreshable Braille Display
// Made for Sprint 2
// Move to next cell, stop, activate, pause, repeat
#include <Servo.h>
#include <Stepper.h>
#include <Wire.h>

// Defining play/pause button info
const int buttonPin = 2;     // the number of the pushbutton pin
const uint16_t DEBOUNCE_INTERVAL = 10;
uint32_t debounce_time;
bool SW1_went_back_low;
int buttonState = 0;         // variable for reading the pushbutton status
bool pause = false;

// Braille 1/2 switch
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
const int stepsToCell = 1000; //TODO determine actual value using beltCalibration program, stepsToCell == n
Stepper belt = Stepper(stepsPerRevolution, stepPin, dirPin);


//Defining cam positions
//TODO Check and edit these
int A = 90; //0 0, 165 is start (right most) and 120 is end (left most)
int B = 180; //1 1
int C = 175; //0 1
int D = 110; //1 0
int z = 0;

//defining for 2-way communication
const byte numChars = 64;
char receivedChars[numChars];
boolean newData = false;

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(57600);
  Serial.begin(115200);

  // attaching servos
  cam1.attach(3);  // listens to pin 9
  cam2.attach(5);  // listens to pin 10
  cam3.attach(6);  // listens to pin 11

  // setting speed of stepper motor for belt
  belt.setSpeed(10); //TODO determine speed

  // Button info / timing
//  timer = millis();
//  debounce_time = timer;
  SW1_went_back_low=true;
}

bool gradeOfBraille() {
  // Braille 1 vs. Braille 2
  switchBraille1 = digitalRead(switchPin);
  if (switchBraille1 == HIGH) {
    braille1 = true;
  }
  else if (switchBraille1 == LOW) {
    braille1 = false;
  }
  
 return braille1;
}

void sendGradeToPython(bool braille1) {
  // TODO check if send button was pressed in python
  if (braille1 == true) {
    Serial.println(2);
  }
  if (braille1 == false) {
    Serial.println(3);
  }
}

void loop() {
  uint32_t t;
  bool SW1_high;
  t = millis();
  
//if (t >= debounce_time + DEBOUNCE_INTERVAL) {
//  SW1_high = digitalRead(buttonPin) == HIGH; 
//  if (SW1_went_back_low && SW1_high) {
//    // Whatever we want when we press the button!
//    Serial.println("Button press");
//    pause = !pause;
//    SW1_went_back_low = false;
//  }
//    
//  else if (!SW1_went_back_low && !SW1_high) {
//    // TODO figure out if this is default case
//    SW1_went_back_low = true;
//  }
//  debounce_time = t;
//  }


if (pause == false) {
  // CODE THAT GOES BRRRR
  
  braille1 = gradeOfBraille();
  sendGradeToPython(braille1);
  
  belt.step(stepsToCell); //move to next cell
  
  recvWithStartEndMarkers(); //receive next character
    
  moveServos();
      
  delay(2000); // could be lower
  replyToPython();
  }
}

void moveServos() {
    //move the servos
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
