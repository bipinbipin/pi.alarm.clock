#!/usr/bin/python

import time
import datetime
import RPi.GPIO as GPIO

from Adafruit_LED_Backpack import SevenSegment

class AlarmClock:

    def __init__(self):
        encoder = RotaryEncoder(self.ENCODER_A, self.ENCODER_B, callback=self.on_turn)
        # Continually update the time on a 4 char, 7-segment display
        while (True):

            # print("alarm check", getCurrentTime())

            # first check if its alarm time needs to be a isolated loop
            if self.getCurrentTime() == self.ALARM_1:
                print("Alarm 1 Triggered.")
                GPIO.output(13, GPIO.HIGH)

            # check all buttons
            if GPIO.input(4) == False:
                print("Button 4 Pressed.")
                self.displayAlarm(self.ALARM_1)

            elif GPIO.input(5) == False:
                print("Encoder 1 Pressed.")
                GPIO.output(13, GPIO.HIGH)
                self.displayAlarm(self.ALARM_1)
                # alarm1 = getTime(stdscr)
                # print(alarm1)
                # displayAlarm(alarm1)
                # time.sleep(1)

            elif GPIO.input(6) == False:
                print("Button 6 Pressed.")
                # GPIO.output(13, GPIO.HIGH)

            else:
                # os.system('echo "no button pressed\n"')
                GPIO.output(13, GPIO.LOW)
                # displayAlarm(ALARM_1)
                # displayCurrentTime()

            # if (GPIO.input(6) == False):
            #     os.system('echo "button 6"')
            #     setAlarm = input("Enter Alarm Time");
            #     # print "Alarm time is now" + str(setAlarm);
            #     displayAlarm(setAlarm)
            # else:
            #     displayCurrentTime()

            # go into SETUP mode

            # displayAlarm(alarm1)
            # # take input and print to screen
            # alarm1 = getTime(stdscr)
            # print(alarm1)

            # Wait a quarter second (less than 1 second to prevent colon blinking getting$
            # Effectively the latency on the inputs
            time.sleep(0.1)

    # Encoder PINS
    ENCODER_A = 17
    ENCODER_B = 22

    # Minute Buffer
    MINUTE_MIN = 00
    MINUTE_MAX = 59

    # 7 Segment I2C Address
    segment = SevenSegment.SevenSegment(address=0x70)


    # GPIO Setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
    GPIO.setup(5, GPIO.IN)
    GPIO.setup(6, GPIO.IN)
    GPIO.setup(13, GPIO.OUT)

    # Alarm
    ALARM_1 = "0000"
    ALARM_2 = 0

    # Initialize the display. Must be called once before using the display.
    segment.begin()

    print("Press CTRL+Z to exit")

    def getNextSeqNum(number):
        number += 1
        return format(number, '04d')


    def on_turn(self, delta):
        print("encoder turned")
        print(delta)
        if delta == 1:
            self.displayAlarm(self.getNextSeqNum(self.ALARM_2))

        elif delta == -1:
            self.displayAlarm(self.getNextSeqNum(self.ALARM_2))





    def displayAlarm(self, time):
        self.segment.clear()
        d = 0
        for i in str(time):
            self.segment.set_digit(d, int(i))
            d = d + 1

        # Toggle colon
        self.segment.set_colon(2)
        self.segment.write_display()

    def displayCurrentTime(self):
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second

        self.segment.clear()
        # Set hours
        self.segment.set_digit(0, int(hour / 10))
        self.segment.set_digit(1, hour % 10)
        # Set minutes
        self.segment.set_digit(2, int(minute / 10))
        self.segment.set_digit(3, minute % 10)
        # Toggle colon
        self.segment.set_colon(second % 2)

        self.segment.write_display()

    def getCurrentTime(self):
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        return str(hour) + str(minute)

    def getTime(self, stdscr):
        newAlarm = ""
        while(len(newAlarm) < 4):
            # key = getKey(stdscr)
            key = ""
            # if len(newAlarm) >= 4:
            #     return newAlarm
            if(isinstance(key, int)):
                newAlarm = newAlarm + str(key)
                # print(newAlarm)
            # elif key == 'ENTER':
            #     return newAlarm
        if(self.isValidTime(newAlarm)):
            return newAlarm
        else:
            self.displayAlarm("8888")
            self.getTime(stdscr)

    def isValidTime(input):
        try:
            time.strptime(input, '%H%M')
            return True
        except ValueError:
            print("Not Valid Time")
            return False


    # def getKey(stdscr):
    #     # Store the key value in the variable `c`
    #     c = stdscr.getch()
    #     # Clear the terminal
    #     # stdscr.clear()
    #     if c == 113:
    #         return 1
    #     elif c == 114:
    #         return 2
    #     elif c == 115:
    #         return 3
    #     elif c == 116:
    #         return 4
    #     elif c == 117:
    #         return 5
    #     elif c == 118:
    #         return 6
    #     elif c == 119:
    #         return 7
    #     elif c == 120:
    #         return 8
    #     elif c == 121:
    #         return 9
    #     elif c == 112:
    #         return 0
    #     elif c == curses.KEY_ENTER:
    #         return 'ENTER'


    # def main(stdscr):
        # clear the screen.. needed?
    GPIO.output(13, GPIO.LOW)
    # stdscr.clear()





    # # wrapper is a function that does all of the setup and teardown, and makes sure
    # # your program cleans up properly if it errors!
    # wrapper(main)


class RotaryEncoder:
    """
    A class to decode mechanical rotary encoder pulses.
    Ported to RPi.GPIO from the pigpio sample here:
    http://abyz.co.uk/rpi/pigpio/examples.html
    """

    def __init__(self, gpioA, gpioB, callback=None, buttonPin=None, buttonCallback=None):
        """
        Instantiate the class. Takes three arguments: the two pin numbers to
        which the rotary encoder is connected, plus a callback to run when the
        switch is turned.

        The callback receives one argument: a `delta` that will be either 1 or -1.
        One of them means that the dial is being turned to the right; the other
        means that the dial is being turned to the left. I'll be damned if I know
        yet which one is which.
        """

        self.lastGpio = None
        self.gpioA = gpioA
        self.gpioB = gpioB
        self.callback = callback

        self.gpioButton = buttonPin
        self.buttonCallback = buttonCallback

        self.levA = 0
        self.levB = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpioB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.gpioA, GPIO.BOTH, self._callback)
        GPIO.add_event_detect(self.gpioB, GPIO.BOTH, self._callback)

        if self.gpioButton:
            GPIO.setup(self.gpioButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self.gpioButton, GPIO.FALLING, self._buttonCallback, bouncetime=500)

    def destroy(self):
        GPIO.remove_event_detect(self.gpioA)
        GPIO.remove_event_detect(self.gpioB)
        GPIO.cleanup()

    def _buttonCallback(self, channel):
        self.buttonCallback(GPIO.input(channel))

    def _callback(self, channel):
        level = GPIO.input(channel)
        if channel == self.gpioA:
            self.levA = level
        else:
            self.levB = level

        # Debounce.
        if channel == self.lastGpio:
            return

        # When both inputs are at 1, we'll fire a callback. If A was the most
        # recent pin set high, it'll be forward, and if B was the most recent pin
        # set high, it'll be reverse.
        self.lastGpio = channel
        if channel == self.gpioA and level == 1:
            if self.levB == 1:
                self.callback(1)
        elif channel == self.gpioB and level == 1:
            if self.levA == 1:
                self.callback(-1)