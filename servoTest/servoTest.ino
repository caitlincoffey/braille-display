/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

// Defining servos
Servo cam1;
Servo cam2;
Servo cam3;

int pos = 0;    // variable to store the servo position

void setup() {
    // attaching servos
  cam1.attach(3);  // listens to pin 9
  cam2.attach(5);  // listens to pin 10
  cam3.attach(6);  // listens to pin 11
}

void loop() {
  cam1.write(145);
  cam2.write(145);
  cam3.write(145);
//  cam1.write(0);
//  cam2.write(0);
//  cam3.write(0);
}
