#!/usr/bin/env python
import os
import sys
from math import sqrt, pow
import json
from time import sleep
from struct import unpack
import subprocess
import Adafruit_LSM303
from influxdb import InfluxDBClient

# Maximum readings
# x (-2048, 2047) y (-2048, 2047) z (-1740, 1780)

class SleepDebugger(object):

    WINDOW_SIZE = 25
    MAG_THRESHOLD = .75
    INFLUX_HOST = "10.1.1.2"
    INFLUX_PORT = 8086
    address = 0x1d
    def __init__(self, filename=None):

        self.lsm303 = Adafruit_LSM303.LSM303(busnum=1, accel_address=0x1d, mag_address=0x6b)
        self.influx = InfluxDBClient(self.INFLUX_HOST, self.INFLUX_PORT, "root", "root", "sleep")

        self.last_point = None
        self.points = []
        self.filename = filename

        self.mag_threshold2 = pow(self.MAG_THRESHOLD, 2)

    def _read_data_point(self):
        accel, mag = self.lsm303.read()
        return accel

    def _notify(self, mag):
        if self.filename:
            subprocess.Popen(['aplay', self.filename])

        json_body = [
            {
                "measurement": "sleep",
                "tags": 
                {
                    "sleeper": "mayhem",
                },
                "fields": 
                {
                    "mag": mag,
                }
            }
        ]
        self.influx.write_points(json_body)

    def _handle_sum(self):

        sum = [0.0, 0.0, 0.0]
        for pt in self.points:
            sum[0] += pt[0]
            sum[1] += pt[1]
            sum[2] += pt[2]

        sum[0] /= len(self.points)
        sum[1] /= len(self.points)
        sum[2] /= len(self.points)

        mag2 = pow(sum[0], 2) + pow(sum[1], 2) + pow(sum[2], 2)
        if mag2 > self.mag_threshold2:
            self._notify(sqrt(mag2))

        self.points = []

    def _handle_point(self, point):
        diff = ( abs(self.last_point[0] - point[0]), abs(self.last_point[1] - point[1]),  abs(self.last_point[2] - point[2]) )
        # print "pt: ", point, " diff: ", diff
        self.points.append(diff)
        if len(self.points) >= self.WINDOW_SIZE:
            self._handle_sum()

        self.last_point = point

    def run(self):
        # There used to be an overrun check, but it turns out that in anything
        # but the steady state, we can't keep up with a 160Hz sample rate. 
        # shouldn't be a problem.
        while True:
            pt = self._read_data_point()
            if not self.last_point:
                self.last_point = pt
                continue
            
            self._handle_point(pt)
            sleep(.005)

if __name__ == "__main__":

    wav = None
    if len(sys.argv) == 2:
        wav = sys.argv[1]

    sd = SleepDebugger(wav)
    try:
        sd.run()
    except KeyboardInterrupt:
        pass
