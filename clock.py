#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import argparse
import sys, traceback
from pythonosc import dispatcher
from pythonosc import osc_server

STEP_DELAY = 0.0030     # delay between steps 
STEPS_24HRS = 3550      # total number of steps in 24 hours on the clock face

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

OSC_LISTEN = "0.0.0.0"  # default listen on address (0.0.0.0 = all)
OSC_PORT = 5005         # default listen on address (0.0.0.0 = all)

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

def forward_handler(unused_addr, args, time):
    print("forward {}".format(args))

def backward_handler(unused_addr, args, time):
    print("backward {}".format(args))

def preset_handler(unused_addr, args):
    print("preset {}".format(args))

def stop_handler(unused_addr, args):
    print("stop {}".format(args))

def main():
    try:
        d = dispatcher.Dispatcher()
        d.map("/forward", forward_handler, "Clock forwards")
        d.map("/backward", backward_handler, "Clock backwards")
        d.map("/preset", preset_handler, "Clock forwards until stopped - preset to midday")
        d.map("/stop", stop_handler, "Stop clock")

        server = osc_server.ThreadingOSCUDPServer((OSC_LISTEN, OSC_PORT), d)
        print("OSC listening on {} port {}".format(OSC_LISTEN, OSC_PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print("Closing down")
        setStep(0,0,0,0)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        setStep(0,0,0,0)

    # We'll never get here!
    sys.exit(0)

if __name__ == "__main__":
    main()

