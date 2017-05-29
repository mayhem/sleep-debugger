#!/usr/bin/env python
import os
import sys
from atexit import register
from time import sleep, time
from sleepdebugger.process_lock import ProcessLock
from sleepdebugger.accelerometer import AccelerometerReader
from sleepdebugger.light_sensor import LightSensorReader
from sleepdebugger.temp_hum_sensor import TempHumSensorReader
from sleepdebugger.radar_sensor import RadarSensorReader
from sleepdebugger.reader import CannotReadSensor
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

        self.radar = None
        if config.RADAR_SENSOR:
            self.radar = RadarSensorReader("radar_sensor", config.RADAR_SENSOR)
            self.radar_time = 0

    def run(self):
        while True:
            sleep_until = sys.maxint
            if self.light and (not self.light_time or time() >= self.light_time):
                try:
                    self.light.read()
                    self.light_time = time() + config.LIGHT_SENSOR_SAMPLE_PERIOD
                except CannotReadSensor as err:
                    print str(err)
                    self.light_time += 1
                if sleep_until > self.light_time:
                    sleep_until = self.light_time

            if self.temphum and (not self.temphum_time or time() >= self.temphum_time):
                try:
                    self.temphum.read()
                    self.temphum_time = time() + config.TEMP_HUM_SENSOR_SAMPLE_PERIOD
                except CannotReadSensor as err:
                    self.temphum_time += 1
                if sleep_until > self.temphum_time:
                    sleep_until = self.temphum_time

            if self.accel and (not self.accel_time or time() >- self.accel_time):
                try:
                    self.accel.read()
                    self.accel_time = time() + (1.0 / config.ACCEL_SAMPLES_PER_SECOND)
                except CannotReadSensor as err:
                    self.accel_time += (1.0 / config.ACCEL_SAMPLES_PER_SECOND)
                if sleep_until > self.accel_time:
                    sleep_until = self.accel_time

            if self.radar and (not self.radar_time or time() >= self.radar_time):
                try:
                    self.radar.read()
                    self.radar_time = time() + config.RADAR_SENSOR_SAMPLE_PERIOD
                except CannotReadSensor as err:
                    self.radar_time += 1
                if sleep_until > self.radar_time:
                    sleep_until = self.radar_time

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
