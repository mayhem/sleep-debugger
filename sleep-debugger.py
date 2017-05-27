#!/usr/bin/env python
import os
import sys
from atexit import register
from time import sleep, time
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
            self.accel_time = 0

        self.light = None
        if config.LIGHT_SENSOR:
            self.light = LightSensorReader("light_sensor", config.LIGHT_SENSOR)
            self.light_time = 0

        self.temphum = None
        if config.TEMP_HUM_SENSOR:
            self.temphum = TempHumSensorReader("temp_hum_sensor", config.TEMP_HUM_SENSOR)
            self.temphum_time = 0

    def run(self):
        while True:
            if self.light and (not self.light_time or time() >= self.light_time):
                self.light.read()
                self.light_time = time() + config.LIGHT_SENSOR_SAMPLE_PERIOD

            if self.temphum and (not self.temphum_time or time() >= self.temphum_time):
                self.temphum.read()
                self.temphum_time = time() + config.TEMP_HUM_SAMPLE_PERIOD

            if self.accel and (not self.accel_time or time() >- self.accel_time):
                self.accel.read()
                self.accel_time = time() + (1.0 / config.ACCEL_SAMPLES_PER_SECOND)

            # Improve this
            sleep(.0005)


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
