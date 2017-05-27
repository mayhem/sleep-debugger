#!/usr/bin/env python
import os
import sys
from atexit import register
from time import sleep
from sleepdebugger.process_lock import ProcessLock
from sleepdebugger.accelerometer import AccelerometerReader
from sleepdebugger.light_sensor import LightSensorReader
from sleepdebugger.temp_hum_sensor import TempHumSensorReader
import sleepdebugger.config as config

LOCK_FILE = "/var/lock/sleep-debugger.lock"

class SleepDebugger(object):

    def __init__(self, filename=None):
        self.lock = ProcessLock(LOCK_FILE)
        if not self.lock.allowed_to_start():
            sys.exit(-1)
        self.lock.create()

        self.accel = None
        if config.ACCEL_SENSOR:
            self.accel = AccelerometerReader("accelerometer", config.ACCEL_SENSOR)

        self.light = None
        if config.LIGHT_SENSOR:
            self.light = LightSensorReader("light_sensor", config.LIGHT_SENSOR)
sefl

        self.temphum = None
        if config.TEMP_HUM_SENSOR:
            self.temphum = TempHumSensorReader("temp_hum_sensor", config.TEMP_HUM_SENSOR)

    def run(self):
        while True:
            if self.light:
                self.light.read()
            if self.temphum:
                self.temphum.read()
            sleep(config.LIGHT_SENSOR_SAMPLE_PERIOD)


if __name__ == "__main__":

    wav = None
    if len(sys.argv) == 2:
        wav = sys.argv[1]

    print "starting sleep debugger accelerometer logger"
    sd = SleepDebugger(wav)
    try:
        sd.run()
    except KeyboardInterrupt:
        pass
