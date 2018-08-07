#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

SENSORPIN = 24
LEDPIN = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(SENSORPIN, GPIO.IN)
GPIO.setup(LEDPIN, GPIO.OUT)

GPIO.output(LEDPIN, 1)

while True:
    print(GPIO.input(SENSORPIN))
    time.sleep(0.25)

