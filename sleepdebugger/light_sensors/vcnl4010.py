#!/usr/bin/env python

import Adafruit_VCNL40xx
from sleepdebugger.reader import CannotLoadSensor, CannotReadSensor

class Sensor(object):

    def __init__(self):
        try:
            self.vcnl = Adafruit_VCNL40xx.VCNL4010(busnum=1)
        except Exception as err:
            raise CannotLoadSensor("Cannot load sensor: %s" % str(err))

    def read(self):
        try:
            return self.vcnl.read_ambient()
        except Exception as err:
            raise CannotReadSensor("Cannot read sensor: %s" % str(err))
