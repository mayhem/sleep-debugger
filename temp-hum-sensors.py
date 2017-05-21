#!/usr/bin/env python
import os
import sys
from atexit import register
from math import sqrt, pow
import json
from subprocess import check_output
from time import sleep, time
from struct import unpack
from influxdb import InfluxDBClient
from sensor_lock import SensorLock

LOCK_FILE = "/var/lock/sleep-debugger-temp-hum-sensor.lock"

class LightSensor(object):

    INFLUX_HOST = "10.1.1.2"
    INFLUX_PORT = 8086
    def __init__(self):

        self.influx = InfluxDBClient(self.INFLUX_HOST, self.INFLUX_PORT, "root", "root", "sleep")
        self.lock = SensorLock(LOCK_FILE)

    def _read_data_point(self):

        line = check_output(["htu21dflib"])
        if line.startswith("#"):
            print "Error: %s" % line[1:]
            return None

        temp, hum = line.split(" ")
        try:
            temp = float(temp)
            hum = float(hum)
        except ValueError:
            print "Invalid data returned from sensor."
            return None

        return (temp, hum)

    def _log(self, temp, hum):
        json_body = [
            {
                "measurement": "temperature",
                "tags": 
                {
                    "sleeper": "mayhem",
                },
                "fields": 
                {
                    "temperature": temp,
                }
            }
        ]
        self.influx.write_points(json_body)
        json_body = [
            {
                "measurement": "humidity",
                "tags": 
                {
                    "sleeper": "mayhem",
                },
                "fields": 
                {
                    "humidity": hum,
                }
            }
        ]
        self.influx.write_points(json_body)

    def run(self):
        if not self.lock.allowed_to_start():
            sys.exit(-1)

        self.lock.create()

        while True:
            temp, hum = self._read_data_point()
            self._log(temp, hum)
            sleep(10)

if __name__ == "__main__":

    print "starting sleep debugger temperature humidity sensor logger"
    ls = LightSensor()
    try:
        ls.run()
    except KeyboardInterrupt:
        pass
