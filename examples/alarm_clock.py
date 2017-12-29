#!/usr/bin/python

import time
import datetime
import os
import RPi.GPIO as GPIO

from lib import SevenSegment

# ===========================================================================
# Clock Example
# ===========================================================================
segment = SevenSegment.SevenSegment(address=0x70)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(13, GPIO.OUT)

# Initialize the display. Must be called once before using the display.
segment.begin()

print("Press CTRL+Z to exit")

setAlarm = "0745"

def displayAlarm(time):
    segment.clear()
    d = 0
    for i in str(time):
        segment.set_digit(d, int(i))
        d = d + 1

    segment.write_display()

def displayCurrentTime():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    segment.clear()
    # Set hours
    segment.set_digit(0, int(hour / 10))
    segment.set_digit(1, hour % 10)
    # Set minutes
    segment.set_digit(2, int(minute / 10))
    segment.set_digit(3, minute % 10)
    # Toggle colon
    segment.set_colon(second % 2)

    segment.write_display()


# Continually update the time on a 4 char, 7-segment display
while(True):

    if (GPIO.input(5) == False):
        os.system('echo "button 5"')
        GPIO.output(13, GPIO.HIGH)
    else:
        GPIO.output(13, GPIO.LOW)

    if (GPIO.input(6) == False):
        os.system('echo "button 6"')
        setAlarm = input("Enter Alarm Time");
        # print "Alarm time is now" + str(setAlarm);
        displayAlarm(setAlarm)
    else:
        displayCurrentTime()

    if (GPIO.input(4) == False):
        displayAlarm(setAlarm)
    else:
        displayCurrentTime()

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    # segment.write_display()

    # Wait a quarter second (less than 1 second to prevent colon blinking getting$
    time.sleep(0.25)
