#!/usr/bin/python

import time
import datetime
import os
import RPi.GPIO as GPIO
import curses

from curses import wrapper
from Adafruit_LED_Backpack import SevenSegment

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



def displayAlarm(time):
    segment.clear()
    d = 0
    for i in str(time):
        segment.set_digit(d, int(i))
        d = d + 1

    # Toggle colon
    segment.set_colon(2)
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

def getTime(stdscr):
    newAlarm = ""
    while(len(newAlarm) < 4):
        key = getKey(stdscr)
        # if len(newAlarm) >= 4:
        #     return newAlarm
        if(isinstance(key, int)):
            newAlarm = newAlarm + str(key)
            # print(newAlarm)
        # elif key == 'ENTER':
        #     return newAlarm
    return newAlarm


def getKey(stdscr):
    # Store the key value in the variable `c`
    c = stdscr.getch()
    # Clear the terminal
    # stdscr.clear()
    if c == 113:
        return 1
    elif c == 114:
        return 2
    elif c == 115:
        return 3
    elif c == 116:
        return 4
    elif c == 117:
        return 5
    elif c == 118:
        return 6
    elif c == 119:
        return 7
    elif c == 120:
        return 8
    elif c == 121:
        return 9
    elif c == 112:
        return 0
    elif c == curses.KEY_ENTER:
        return 'ENTER'

def main(stdscr):
    # clear the screen.. needed?
    stdscr.clear()
    alarm1 = "0745"

    # Continually update the time on a 4 char, 7-segment display
    while(True):


        if (GPIO.input(5) == False):
            # os.system('echo "button 5"')
            displayAlarm(alarm1)
            GPIO.output(13, GPIO.HIGH)
            alarm1 = getTime(stdscr)
            print(alarm1)
        else:
            GPIO.output(13, GPIO.LOW)
            displayCurrentTime()

        # if (GPIO.input(6) == False):
        #     os.system('echo "button 6"')
        #     setAlarm = input("Enter Alarm Time");
        #     # print "Alarm time is now" + str(setAlarm);
        #     displayAlarm(setAlarm)
        # else:
        #     displayCurrentTime()

        # go into SETUP mode
        if (GPIO.input(4) == False):
            # displayAlarm(alarm1)
            # # take input and print to screen
            # alarm1 = getTime(stdscr)
            # print(alarm1)
            displayAlarm(alarm1)
        else:
            displayCurrentTime()

        # Write the display buffer to the hardware.  This must be called to
        # update the actual display LEDs.
        # segment.write_display()

        # Wait a quarter second (less than 1 second to prevent colon blinking getting$
        # Effectively the latency on the inputs
        time.sleep(0.1)

# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)