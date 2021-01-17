#!/usr/bin/python
import os
import time
import Adafruit_BBIO.GPIO as GPIO

def hwports():
    for portno in range(0, 25):
        port = 'P8_' + str(portno)
        yield port

for port in hwports():
    GPIO.setup(port, GPIO.IN)

while True:
    os.system('clear')
    for port in hwports():
        value = GPIO.input(port)
        print(port, value)
    time.sleep(0.2)
