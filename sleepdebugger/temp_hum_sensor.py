#!/usr/bin/env python
import os
import sys
from sleepdebugger.reader import Reader

class TempHumSensor(Reader):

    def __init__(self, type, model):
        super(Reader, self).__init__(type, model)

    def read(self):
        temp, hum = self.sensor.read()
        print "temp hum sensor: %.2f %.2f" % (temp, hum)
        self._save_data({ 'humidity' : hum, 'temperature' : temp })
