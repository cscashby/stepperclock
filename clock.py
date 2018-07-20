#!/usr/bin/python
import RPi.GPIO as GPIO
import time


STEP_DELAY = 0.0030     # delay between steps 
STEPS_24HRS = 3550      # total number of steps in 24 hours on the clock face

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# NOTE no need for enable pins; they can be constantly pulled high
# IN1-4 to control step sequence
COIL_A_1_PIN = 17
COIL_A_2_PIN = 18
COIL_B_1_PIN = 22
COIL_B_2_PIN = 23

# Set pin states
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Function for step sequence
def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

def runBackward(steps):
    for i in range(0, steps):
        setStep(1,0,1,0)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(0,1,0,1)
        time.sleep(delay)
        setStep(1,0,0,1)
        time.sleep(delay)

def runForward(steps):
    for i in range(0, steps):
        setStep(1,0,0,1)
        time.sleep(delay)
        setStep(0,1,0,1)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(1,0,1,0)
        time.sleep(delay)

setStep(0,0,0,0)

