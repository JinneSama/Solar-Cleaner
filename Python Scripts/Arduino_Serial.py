#!/usr/bin/env python
print("Content-type: text/html")
print("")
print("<html><body>")
print("<h1>Cleaning Started</h1>")

import serial
import time

port = '/dev/ttyACM0'
baud_rate = 9600

ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)

def send_data(data):
    ser.write(data.encode())

send_data("HOME_X,PUMP_ON,X_CCW 5000,X_CW 5000,X_CCW 5000,X_CW 5000,Y_CW 2000,X_CCW 5000,PUMP_OFF,HOME_X")
ser.close()

print("</body></html>")
