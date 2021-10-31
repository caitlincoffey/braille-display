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

void setup() {
  // put your setup code here, to run once:
  // setting up servos
  cam1.attach(9);  // listens to pin 9
  cam2.attach(10);  // listens to pin 10
  cam2.attach(11);  // listens to pin 11
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
//  if (Serial.available()) {
//      // ewwww this int conversion 
//      String a = Serial.readString();
//      Serial.print("Received Value: ");
//      Serial.println(a);
//      int b = a.toInt();
//  }
}
