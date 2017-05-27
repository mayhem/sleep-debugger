#!/usr/bin/env python
import os
import sys
from atexit import register
from time import sleep
from sleepdebugger.sensor_lock import SensorLock
from sleepdebugger.accelerometer import AccelerometerReader
from sleepdebugger.light_sensor import LightSensorReader

LOCK_FILE = "/var/lock/sleep-debugger.lock"

class SleepDebugger(object):

    def __init__(self, filename=None):
        self.lock = SensorLock(LOCK_FILE)
        self.lock.create()
        if not self.lock.allowed_to_start():
            sys.exit(-1)

        self.accel = None
        if config.ACCEL_SENSOR:
            self.accel = AccelerometerReader("accelometer", config.ACCEL_SENSOR)

        self.light = None
        if config.LIGHT_SENSOR:
            self.light = LightSensorReader("light_sensor", config.LIGHT_SENSOR)

    def run(self):
        while True:
            self.light.read()
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
