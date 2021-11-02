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

void setup() {
  // put your setup code here, to run once:
  // setting up servos
  cam1.attach(6);  // listens to pin 9
  cam2.attach(10);  // listens to pin 10
  cam3.attach(11);  // listens to pin 11
  cam1.write(A);
  cam2.write(A);
  cam3.write(A);
//  Serial.begin(57600);
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    // read the incoming byte:
    String cmd = Serial.readString();
    Serial.println(cmd);
    cam1.write(cmd.charAt(0));
    cam2.write(cmd.charAt(1));
    cam3.write(cmd.charAt(2));
    while(Serial.available() > 0) {
      Serial.read();
    }
    delay(500);
    Serial.write(1);
//    incomingByte = Serial.read();
//
//    // say what you got:
//    Serial.print("I received: ");
//    Serial.println(incomingByte, DEC);
//  }
//  if (Serial.available()) {
//      // ewwww this int conversion 
//      String a = Serial.readString();
//      Serial.print("Received Value: ");
//      Serial.println(a);
//      int b = a.toInt();
////  }
  }
}
