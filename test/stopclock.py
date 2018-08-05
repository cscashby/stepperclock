#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Variables
# 0.0055
delay = 0.0030
steps = 3550

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Enable GPIO pins for  ENA and ENB for stepper

#enable_a = 14
#enable_b = 15

# Enable pins for IN1-4 to control step sequence

coil_A_1_pin = 17
coil_A_2_pin = 18
coil_B_1_pin = 22
coil_B_2_pin = 23

# Set pin states

#GPIO.setup(enable_a, GPIO.OUT)
#GPIO.setup(enable_b, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Set ENA and ENB to high to enable stepper

#GPIO.output(enable_a, True)
#GPIO.output(enable_b, True)

# Function for step sequence

def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

setStep(0,0,0,0)

