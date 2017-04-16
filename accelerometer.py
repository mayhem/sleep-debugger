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
from pykalman import KalmanFilter

# Maximum readings
# x (-2048, 2047) y (-2048, 2047) z (-1740, 1780)

class SleepDebugger(object):

    WINDOW_SIZE = 25
    MAG_THRESHOLD = 4.0
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
        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        self.point = None
        self.covariance = [ [0.0], [0.0], [0.0] ]

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

    def _handle_point(self, raw_point):

        if not self.point:
            self.point = raw_point

        (self.point[0], self.covariance[0]) = self.kf.filter_update(self.point[0], self.covariance[0], raw_point[0])
        (self.point[1], self.covariance[1]) = self.kf.filter_update(self.point[1], self.covariance[1], raw_point[1])
        (self.point[2], self.covariance[2]) = self.kf.filter_update(self.point[2], self.covariance[2], raw_point[2])

        point = [self.point[0][0].data[0], self.point[1][0].data[0], self.point[2][0].data[0]]

        diff = ( abs(self.last_point[0] - point[0]), abs(self.last_point[1] - point[1]),  abs(self.last_point[2] - point[2]) )
#        print "pt: ", point, " diff: ", diff

        mag2 = pow(diff[0], 2) + pow(diff[1], 2) + pow(diff[2], 2)
        if mag2 > self.mag_threshold2:
            self._notify(sqrt(mag2))

        self.last_point = point

    def run(self):
        # There used to be an overrun check, but it turns out that in anything
        # but the steady state, we can't keep up with a 160Hz sample rate. 
        # shouldn't be a problem.
        while True:
            pt = list(self._read_data_point())
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
