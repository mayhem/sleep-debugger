import os
import sys
import RPi.GPIO as gpio
from time import sleep

class Sensor(object):

    input_pin = 20
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.input_pin, gpio.IN)

    def read(self):
        if gpio.input(self.input_pin) == gpio.HIGH:
            return 1.0
        else:
            return 0.0

s = Sensor()
while True:
    print s.read()
    sleep(1)
