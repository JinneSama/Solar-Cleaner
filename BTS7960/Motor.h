#define X_Motor 10
#define X_L_EN 8
#define X_R_EN 9

#define Y_Motor 11
#define Y_L_EN 12
#define Y_R_EN 13

#define X_Limit 4
#define Y_Limit 5

void initMotor() {
  pinMode(X_Motor, OUTPUT);
  pinMode(Y_Motor, OUTPUT);
  pinMode(X_L_EN,OUTPUT);
  pinMode(X_R_EN,OUTPUT);
  pinMode(Y_R_EN,OUTPUT);
  pinMode(Y_L_EN,OUTPUT);
  pinMode(X_Limit,INPUT_PULLUP);
  pinMode(Y_Limit,INPUT_PULLUP);

  //8Khz Frequency on Pin 11 and 12
  TCCR1A = (1 << WGM10) | (1 << COM1A1) | (1 << COM1B1);
  TCCR1B = (1 << WGM12) | (1 << CS10); 
  OCR1A = 125;
  OCR1B = 125;
  TCCR1A |= (1 << CS10);
  TCCR1B |= (1 << CS10);
}

int separateValue(String _received) {
  int _value = 0;
  int spaceIndex = _received.indexOf(' ');
  if (spaceIndex != -1) {
    String valueString = _received.substring(spaceIndex + 1);
    _value = valueString.toInt();
  }
  return _value;
}

void X_Motor_Stop() {
  digitalWrite(X_L_EN,LOW);
  digitalWrite(X_R_EN,LOW);
  delayMicroseconds(100);
  analogWrite(X_Motor , 0);
}

void Y_Motor_Stop() {
  digitalWrite(Y_R_EN,LOW);
  digitalWrite(Y_L_EN,LOW);
  delayMicroseconds(100);
  analogWrite(Y_Motor , 0);
}

void X_Motor_CW(int _runtime) {
  digitalWrite(X_L_EN,HIGH);
  digitalWrite(X_R_EN,LOW);
  delayMicroseconds(100);
  analogWrite(X_Motor , 135);
  delay(_runtime);
  X_Motor_Stop();
}

void X_Motor_CCW(int _runtime) {
  digitalWrite(X_R_EN,HIGH);
  digitalWrite(X_L_EN,LOW);
  delayMicroseconds(100);
  analogWrite(X_Motor , 135);
  delay(_runtime);
  X_Motor_Stop();
}
void Y_Motor_CW(int _runtime) {
  digitalWrite(Y_L_EN,HIGH);
  digitalWrite(Y_R_EN,LOW);
  delayMicroseconds(100);
  analogWrite(Y_Motor , 25);
  delay(_runtime);
  Y_Motor_Stop();
}

void Y_Motor_CCW(int _runtime) {
  digitalWrite(Y_R_EN,HIGH);
  digitalWrite(Y_L_EN,LOW);
  delayMicroseconds(100);
  analogWrite(Y_Motor , 25);
  delay(_runtime);
  Y_Motor_Stop();
}
void Home_X() {
  while(digitalRead(X_Limit)) {
    digitalWrite(X_R_EN,HIGH);
    digitalWrite(X_L_EN,LOW);
    delayMicroseconds(100);
    analogWrite(X_Motor , 135);  
  }
  X_Motor_Stop();
}

void Home_Y() {
  while(digitalRead(Y_Limit)) {
    digitalWrite(Y_R_EN,HIGH);
    digitalWrite(Y_L_EN,LOW);
    delayMicroseconds(100);
    analogWrite(Y_Motor , 130);  
  }
  Y_Motor_Stop();
}

void CommandMotor(String receivedString) {
  if (receivedString.startsWith("X_CCW")) {
    X_Motor_CCW(separateValue(receivedString));
  } else if (receivedString.startsWith("X_CW")) {
    X_Motor_CW(separateValue(receivedString));
  } else if (receivedString.startsWith("Y_CCW")) {
    Y_Motor_CCW(separateValue(receivedString));
  } else if (receivedString.startsWith("Y_CW")) {
    Y_Motor_CW(separateValue(receivedString));
  } else if (receivedString.startsWith("X_STOP")) {
    X_Motor_Stop();
  } else if (receivedString.startsWith("Y_STOP")) {
    Y_Motor_Stop();
  }else if (receivedString.startsWith("HOME_X")) {
    Home_X();
  }else if (receivedString.startsWith("HOME_Y")) {
    Home_Y();
  }
}
