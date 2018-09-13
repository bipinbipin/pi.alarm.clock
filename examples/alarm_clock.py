#!/usr/bin/python

import time
import datetime
import RPi.GPIO as GPIO

from Adafruit_LED_Backpack import SevenSegment
from subprocess import call

class AlarmClock:

    def __init__(self):
        print("Press CTRL+Z to exit")
        encoder = RotaryEncoder(self.ENCODER_A, self.ENCODER_B, callback=self.on_turn)

        # 7 Segment I2C Address
        self.segment = SevenSegment.SevenSegment(address=0x70)

        # Initialize the display. Must be called once before using the display.
        self.segment.begin()
        print("Segment Initialized")

        GPIO.output(13, GPIO.LOW)

        self.mainloop()

    # Encoder PINS
    ENCODER_A = 17
    ENCODER_B = 22
    ENCODER_BUTTON = 5

    # Button PINS
    SET_BUTTON = 6
    CHANGE_ALARM_BUTTON = 4


    # Minute Buffer
    MINUTE_BUFFER = 00
    MINUTE_MIN = 00
    MINUTE_MAX = 59

    # Hour Buffer
    HOUR_BUFFER = 00
    HOUR_MIN = 00
    HOUR_MAX = 23

    # GPIO Setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
    GPIO.setup(5, GPIO.IN)
    GPIO.setup(6, GPIO.IN)
    GPIO.setup(13, GPIO.OUT)

    # Alarm
    ALARM_1 = "0000"

    # Modes
    _MODE_ALARM_ENGAGED = False
    _MODE_SET_TIME = False
    _MODE_SET_TIME_MINUTES = False
    _MODE_SET_TIME_HOURS = False
    _MODE_DISPLAY_TIME = True

    def encoder_button_pressed(self):
        return not GPIO.input(self.ENCODER_BUTTON)

    def set_button_pressed(self):
        return not GPIO.input(self.SET_BUTTON)

    def change_alarm_button_pressed(self):
        return not GPIO.input(self.CHANGE_ALARM_BUTTON)

    def mainloop(self):
        print("Main Loop Executing")

        loop_interval = 0.05
        alarm_expire_time = 0

        while True:

            # CHECK THE MODE
            # CAREFUL TO ONLY HAVE ONE MODE TRUE!!
            if self._MODE_SET_TIME:
                if self._MODE_SET_TIME_HOURS:
                    if self.encoder_button_pressed():
                        self._MODE_SET_TIME_HOURS = False
                        self._MODE_SET_TIME_MINUTES = True
                        time.sleep(0.3)
                    self.display_hours()

                if self._MODE_SET_TIME_MINUTES:
                    if self.encoder_button_pressed():
                        self._MODE_SET_TIME_MINUTES = False
                        self._MODE_SET_TIME = False
                        self.save_alarm()
                    self.display_minutes()

            elif self._MODE_ALARM_ENGAGED:
                if self.encoder_button_pressed():
                    alarm_expire_time = 0
                    self._MODE_ALARM_ENGAGED = False
                    GPIO.output(13, GPIO.LOW)
                else:
                    # ALARM IS HAPPENING!!
                    print("Alarm 1 Triggered.")
                    call(["flite", "wake the fuck up!"])
                    GPIO.output(13, GPIO.HIGH)
                    print(alarm_expire_time)
                    loop_interval = 3

            elif self._MODE_DISPLAY_TIME:
                print(alarm_expire_time)
                # IS IT ALARM TIME?
                # HAS THE ALARM JUST BEEN DISENGAGED?
                if self.current_time() == self.ALARM_1 and not self.current_time() == alarm_expire_time:
                    print("setting expire time: " + alarm_expire_time)
                    alarm_expire_time = self.current_time()
                    self._MODE_ALARM_ENGAGED = True

                # CHANGE ALARM TIME
                if self.change_alarm_button_pressed():
                    print("Button 6 Pressed.")
                    self._MODE_SET_TIME = True
                    self._MODE_SET_TIME_HOURS = True

                # SHOW CURRENT ALARM TIME
                elif self.encoder_button_pressed():
                    print("Encoder 1 Pressed.")
                    self.display_time(self.ALARM_1)

                # SHOW CURRENT TIME
                else:
                    self.displayCurrentTime()
                    loop_interval = 0.05

            time.sleep(loop_interval)

    def on_turn(self, delta):
        # ONLY ACT WHEN IN 'SET TIME' MODE
        if self._MODE_SET_TIME:
            # DETERMINE HOURS OR MINUTE MODE
            if self._MODE_SET_TIME_MINUTES:
                if self.MINUTE_MAX >= (self.MINUTE_BUFFER + delta) >= self.MINUTE_MIN:
                    self.MINUTE_BUFFER += delta
            if self._MODE_SET_TIME_HOURS:
                if self.HOUR_MAX >= (self.HOUR_BUFFER + delta) >= self.HOUR_MIN:
                    self.HOUR_BUFFER += delta

    def display_minutes(self):
        self.segment.clear()
        minutes = str(format(self.MINUTE_BUFFER, '02d'))
        hours = str(format(self.HOUR_BUFFER, '02d'))
        self.display_time(hours + minutes)
        # self.segment.set_digit(2, int(display_string[0]))
        # self.segment.set_digit(3, int(display_string[1]))
        self.segment.set_decimal(2, True)
        self.segment.set_decimal(3, True)
        self.segment.write_display()

    def display_hours(self):
        self.segment.clear()
        display_string = str(format(self.HOUR_BUFFER, '02d'))
        self.segment.set_digit(0, int(display_string[0]))
        self.segment.set_digit(1, int(display_string[1]))
        self.segment.set_decimal(0, True)
        self.segment.set_decimal(1, True)
        self.segment.write_display()

    def save_alarm(self):
        minutes = str(format(self.MINUTE_BUFFER, '02d'))
        hours = str(format(self.HOUR_BUFFER, '02d'))
        self.ALARM_1 = hours + minutes
        print(self.ALARM_1)
        print(self.current_time())

    def display_time(self, time_value):
        self.segment.clear()
        d = 0
        for i in str(time_value):
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

    def current_time(self):
        now = datetime.datetime.now()
        minutes = str(format(now.minute, '02d'))
        hours = str(format(now.hour, '02d'))
        return hours + minutes

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
            self.display_time("8888")
            self.getTime(stdscr)

    def isValidTime(self, input):
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


# call the class to instantiate and run
AlarmClock()
