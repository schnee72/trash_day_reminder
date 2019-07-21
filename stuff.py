#!/usr/bin/env python

import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import sys
import threading
import RPi.GPIO as GPIO
import Adafruit_DHT
from Adafruit_LED_Backpack import SevenSegment
import holidays

us_holidays = holidays.US()
holiday_list = [
    'New Year\'s Day', 
    'New Year\'s Day (Observed)',
    'Memorial Day',
    'Independence Day',
    'Independence Day (Observed)',
    'Labor Day',
    'Thanksgiving',
    'Christmas Day',
    'Christmas Day (Observed)'
]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
BLUE_LED = 18
GREEN_LED = 23
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
left_display = SevenSegment.SevenSegment(address=0x71)
right_display = SevenSegment.SevenSegment(address=0x72)
left_display.begin()
right_display.begin()
sensor = Adafruit_DHT.DHT22
pin = 4
ctr = 0
start_date = datetime(2017, 6, 22, 0, 1, 1)

def update_temp():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if temperature is not None:
        right_display.clear()
        right_display.set_colon(False)
        right_display.print_float(temperature)
        right_display.write_display()

def leds_on(now):
    GPIO.output(BLUE_LED, True)
    first = (start_date - timedelta(days=start_date.weekday()))
    second = (now - timedelta(days=now.weekday()))
    weeks = (first - second).days / 7
    if weeks % 2 == 1:
        GPIO.output(GREEN_LED, True)

def leds_off():
    GPIO.output(BLUE_LED, False)
    GPIO.output(GREEN_LED, False)

def update_time(now): 
    hour = now.hour
    minute = now.minute
    second = now.second
    left_display.clear()
    left_display.set_digit(0, int(hour / 10))
    left_display.set_digit(1, hour % 10)
    left_display.set_digit(2, int(minute / 10))
    left_display.set_digit(3, minute % 10)
    left_display.set_colon(second % 2)
    left_display.write_display()

def holiday_week(day):
    if holiday(day):
        return True      
    else:
        n = -1
        for x in range(0, 3):
            previous_day = day + timedelta(days=n)
            if holiday(previous_day):
                return True
            n -= 1
    return False

def holiday(day):
    hol_test = us_holidays.get(day)
    if hol_test in holiday_list:
        return True
    elif isinstance(hol_test, list):
        return bool(set(holiday_list) & set(us_holidays.get(day)))
    return False

print('Press Ctrl-C to quit.')

try:
    while(True):
        now = datetime.now()
        # once every 30 seconds
        if ctr == 120:
            t = threading.Thread(target=update_temp)
            t.start()
            ctr = 0
            leds_off()
            weekday = now.weekday()
            if weekday == 3:
                # thursday
                if not holiday_week(now):
                    leds_on(now)
            elif weekday == 4:
                # friday
                previous_day = now + timedelta(days=-1)
                if holiday_week(previous_day):
                    leds_on(now)
        update_time(now)
        time.sleep(0.25)
        ctr += 1
finally:
    GPIO.cleanup()
