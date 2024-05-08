#!/usr/bin/python
# -*- coding: utf-8 -*-

from RPi import GPIO
import sys

GPIO_PIN = 18 # BCM
PWM_FREQ = 60 # in hertz
WAIT_TIME = 1 # in seconds

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)#, initial=GPIO.LOW)

fan = GPIO.PWM(GPIO_PIN, PWM_FREQ)
fan.start(0)

try:
    while True:
        load = float(input("Fan Load (0~100) > "))
        fan.ChangeDutyCycle(load)

except(KeyboardInterrupt):
    fan.stop()
    GPIO.cleanup()
    sys.exit()
