#!/usr/bin/env python

import serial
from sleepdebugger.reader import CannotLoadSensor, CannotReadSensor

class Sensor(object):

    DEVICE = "/dev/serial0"
    BAUD_RATE = 9600

    def __init__(self):
        self.ser = None
        try:
            self.ser = serial.Serial(self.DEVICE, self.BAUD_RATE, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.01)
        except serial.serialutil.SerialException, err:
            raise CannotLoadSensor("Cannot load sensor: %s" % str(err))
        except Exception as err:
            raise CannotLoadSensor("Cannot load sensor: %s" % str(err))

    def read(self):
        if not self.ser:
            raise CannotReadSensor("Cannot read sensor.")
        try:
            self.ser.write('*')
            line = self.ser.readline()
        except Exception as err:
            raise CannotReadSensor("Cannot read sensor: %s" % str(err))

        return int(line.strip())
