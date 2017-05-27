#!/usr/bin/env python
import os
import sys
from sleepdebugger.reader import Reader

class TempHumSensorReader(Reader):

    def __init__(self, type, model):
        super(TempHumSensorReader, self).__init__(type, model)

    def read(self):
        temp, hum = self.sensor.read()
        self._save_data('humidity', { 'humidity' : hum })
        self._save_data('temperature', { 'temperature' : temp })
