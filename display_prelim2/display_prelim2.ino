// Preliminary Arduino Driver file for Refreshable Braille Display
#include <Adafruit_MotorShield.h>
#include <Servo.h>

// Define motorshield
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// TODO add stepper motor

// Defining servos
Servo cam1;  // TODO change name
Servo cam2;
Servo cam3;

// Defining pins 
const int button = A0; // Pin for button 

//Defining cam positions
//TODO make these actual servo positions
int A = 145; //0 0, 165 is start (right most) and 120 is end (left most)
int B = 180; //1 1
int C = 175; //0 1
int D = 110; //1 0

//defining for 2-way communication
const byte numChars = 64;
char receivedChars[numChars];
boolean newData = false;

void setup() {
  // put your setup code here, to run once:
  // setting up servos
    //Serial.begin(57600);
  Serial.begin(115200);

  cam1.attach(6);  // listens to pin 9
  cam2.attach(10);  // listens to pin 10
  cam3.attach(11);  // listens to pin 11
  cam1.write(A);
  cam2.write(A);
  cam3.write(A);

  Serial.println("<Arduino is ready>");
  delay(6000); // six second delay for python
}

void loop() {
  // put your main code here, to run repeatedly:
//  if (Serial.available() > 0) {
//    // read the incoming byte:
//    String cmd = Serial.readString();
//    Serial.println(cmd);
//    cam1.write(cmd.charAt(0));
//    cam2.write(cmd.charAt(1));
//    cam3.write(cmd.charAt(2));
//    while(Serial.available() > 0) {
//      Serial.read();
//    }
//    delay(500);
//    Serial.write(1);
//  }

  String val;
//  while (Serial.available() > 0) {
//    val = val + (char)Serial.read(); // read data byte by byte and store it
//  }
  Serial.print(val); // send the received data back to raspberry pi

  //recvWithStartEndMarkers();
//  replyToPython();
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
    Serial.print("Received this!");Serial.println(rc);

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ind] = rc;
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
    Serial.print("Just received ");
    Serial.println(receivedChars);
    newData = false;
    cam1.write(receivedChars[0]);
  }
}
