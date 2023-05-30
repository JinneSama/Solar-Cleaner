#include "Motor.h"
#include "GCode.h"

void setup() {
  Serial.begin(9600);
  initMotor();
}

void loop() {
  if (Serial.available()) {
    String receivedString = Serial.readStringUntil('\n');
    ReadGCodeFromSerial(receivedString);
  }
}
