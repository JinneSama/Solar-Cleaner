int GCode_Size = 0;

void ReadGCodeFromSerial(String _fromSerial) {
  int _length = _fromSerial.length() + 1;
  char _codes[_length];
  _fromSerial.toCharArray(_codes , _length);

  char *code[_length];
  char *ptr = NULL;

  byte index = 0;
  ptr = strtok(_codes , ",");

  while(ptr != NULL){
    code[index] = ptr;
    index++;
    ptr = strtok(NULL , ",");
  }

  for (int i = 0; i < index; i++)
  {
     Serial.print(i);
     Serial.print("  ");
     Serial.println(code[i]);
     CommandMotor(code[i]);
  }
}
