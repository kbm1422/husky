
#include <Stepper.h>

const int stepsPerRevolution = 400;    // change this to fit the number of steps per revolution for your motor
Stepper stepper(stepsPerRevolution, 8,9,10,11);    // initialize the stepper library on pins 8 through 11:

void setup() {
  // set the speed at 60 rpm:
  stepper.setSpeed(120);
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()){
    char c = Serial.read();
    if (c=='F'){
      stepper.step(stepsPerRevolution);
      Serial.println("clockwise");
    }
    else if (c=='B'){
      stepper.step(-stepsPerRevolution);
      Serial.println("counterclockwise");
    }
  }
}

