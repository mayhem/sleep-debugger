#!/usr/bin/env python
import os
import sys
from atexit import register
from time import sleep, time
from sleepdebugger.process_lock import ProcessLock
from sleepdebugger.accelerometer import AccelerometerReader
from sleepdebugger.light_sensor import LightSensorReader
from sleepdebugger.temp_hum_sensor import TempHumSensorReader
from sleepdebugger.reader import CannotReadSensor
import sleepdebugger.config as config

LOCK_FILE = "/var/lock/sleep-debugger.lock"

class SleepDebugger(object):

    def __init__(self, filename=None):
        self.lock = ProcessLock(LOCK_FILE)
        if not self.lock.allowed_to_start():
            sys.exit(-1)
        self.lock.create()

        self.temphum = None
        if config.TEMP_HUM_SENSOR:
            self.temphum = TempHumSensorReader("temp_hum_sensor", config.TEMP_HUM_SENSOR)
            self.temphum_time = 0

    def run(self):
        while True:
            sleep_until = sys.maxint

            if self.temphum and (not self.temphum_time or time() >= self.temphum_time):
                try:
                    self.temphum.read()
                    self.temphum_time = time() + config.TEMP_HUM_SENSOR_SAMPLE_PERIOD
                except CannotReadSensor as err:
                    self.temphum_time += 1
                if sleep_until > self.temphum_time:
                    sleep_until = self.temphum_time

            sleep(max(0, sleep_until - time()))


if __name__ == "__main__":

    wav = None
    if len(sys.argv) == 2:
        wav = sys.argv[1]

    print "starting sleep debugger logger"
    sd = SleepDebugger(wav)
    try:
        sd.run()
    except KeyboardInterrupt:
        pass
