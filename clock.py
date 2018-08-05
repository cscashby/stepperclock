#!/usr/bin/python
import RPi.GPIO as GPIO
import time


STEP_DELAY = 0.0030     # delay between steps 
STEPS_24HRS = 3550      # total number of steps in 24 hours on the clock face

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# NOTE no need for enable PINs; they can be constantly pulled high
# IN1-4 to control step sequence
COIL_A_1_PIN = 17
COIL_A_2_PIN = 18
COIL_B_1_PIN = 22
COIL_B_2_PIN = 23

# Set PIN states
GPIO.setup(COIL_A_1_PIN, GPIO.OUT)
GPIO.setup(COIL_A_2_PIN, GPIO.OUT)
GPIO.setup(COIL_B_1_PIN, GPIO.OUT)
GPIO.setup(COIL_B_2_PIN, GPIO.OUT)

# Function for step sequence
def setStep(w1, w2, w3, w4):
  GPIO.output(COIL_A_1_PIN, w1)
  GPIO.output(COIL_A_2_PIN, w2)
  GPIO.output(COIL_B_1_PIN, w3)
  GPIO.output(COIL_B_2_PIN, w4)

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

