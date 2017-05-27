import os
import sys
import Adafruit_LSM303
from sleepdebugger.reader import CannotLoadSensor, CannotReadSensor

class Sensor(object):

    def __init__(self):
        try:
            self.lsm303 = Adafruit_LSM303.LSM303(busnum=1, accel_address=0x1d, mag_address=0x6b)
        except Exception as err:
            raise CannotLoadSensor("Cannot load sensor: %s" % str(err))

    def read(self):
        try:
            accel, mag = self.lsm303.read()
            return accel
        except Exception as err:
            raise CannotReadSensor("Cannot read sensor: %s" % str(err))
