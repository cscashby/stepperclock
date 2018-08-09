#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import argparse
import sys, traceback
from pythonosc import dispatcher
from pythonosc import osc_server
from subprocess import call

STEP_DELAY = 0.0025     # STEP_DELAY between steps 
STEPS_WAITIR = 50      # Steps to wait until activating IR LED
STEPS_MAX = 1000 # Steps to stop after if IR fails us

OSC_LISTEN = "0.0.0.0"  # default listen on address (0.0.0.0 = all)
OSC_PORT = 5005         # default listen on address (0.0.0.0 = all)

# NOTE no need for enable PINs; they can be constantly pulled high
# IN1-4 to control step sequence
COIL_B_1_PIN = 17
COIL_B_2_PIN = 18
COIL_A_1_PIN = 22
COIL_A_2_PIN = 23

# IR Sensor and Paired LED behind '12' to detect minute hand at zero
IRSENSE_PIN = 24
LED_PIN = 25

# Function for step sequence
def setStep(w1, w2, w3, w4):
  GPIO.output(COIL_A_1_PIN, w1)
  GPIO.output(COIL_A_2_PIN, w2)
  GPIO.output(COIL_B_1_PIN, w3)
  GPIO.output(COIL_B_2_PIN, w4)

def runBackward(steps):
    for i in range(0, steps):
        setStep(1,0,1,0)
        time.sleep(STEP_DELAY)
        setStep(0,1,1,0)
        time.sleep(STEP_DELAY)
        setStep(0,1,0,1)
        time.sleep(STEP_DELAY)
        setStep(1,0,0,1)
        time.sleep(STEP_DELAY)

def runForward(steps):
    for i in range(0, steps):
        setStep(1,0,0,1)
        time.sleep(STEP_DELAY)
        setStep(0,1,0,1)
        time.sleep(STEP_DELAY)
        setStep(0,1,1,0)
        time.sleep(STEP_DELAY)
        setStep(1,0,1,0)
        time.sleep(STEP_DELAY)

def forward_handler(unused_addr, args, hrs):
    print("forward {} for {} hours".format(args, hrs))
    GPIO.output(LED_PIN, 1)
    for i in range(int(hrs)):
        count = 0
        while count < STEPS_WAITIR or GPIO.input(IRSENSE_PIN) == 1:
            count += 1
            runForward(1)
            if count > STEPS_MAX:
                break
    GPIO.output(LED_PIN, 0)
    setStep(0,0,0,0)

def backward_handler(unused_addr, args, hrs):
    print("backward {} for {} hrs".format(args, hrs))
    GPIO.output(LED_PIN, 1)
    for i in range(int(hrs)):
        count = 0
        while count < STEPS_WAITIR or GPIO.input(IRSENSE_PIN) == 1:
            count += 1
            runBackward(1)
            if count > STEPS_MAX:
                break
    GPIO.output(LED_PIN, 0)
    setStep(0,0,0,0)

def shutdown_handler(unused_addr, args, unused_arg):
    print("shutdown {}".format(args))
    setStep(0,0,0,0)
    call("sudo poweroff", shell=True)

def reboot_handler(unused_addr, args, unused_arg):
    print("reboot {}".format(args))
    setStep(0,0,0,0)
    call("sudo reboot", shell=True)

def main():
    try:
        # Set PIN states
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(COIL_A_1_PIN, GPIO.OUT)
        GPIO.setup(COIL_A_2_PIN, GPIO.OUT)
        GPIO.setup(COIL_B_1_PIN, GPIO.OUT)
        GPIO.setup(COIL_B_2_PIN, GPIO.OUT)
        GPIO.setup(IRSENSE_PIN, GPIO.IN)
        GPIO.setup(LED_PIN, GPIO.OUT)

        d = dispatcher.Dispatcher()
        d.map("/forward", forward_handler, "Clock forwards (hours)")
        d.map("/backward", backward_handler, "Clock backwards (hours)")
        d.map("/shutdown", shutdown_handler, "Shutdown Pi nicely")
        d.map("/reboot", reboot_handler, "Reboot Pi nicely")

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

