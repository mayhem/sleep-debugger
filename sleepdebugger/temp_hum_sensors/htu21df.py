#!/usr/bin/env python
import os
import sys
from sleepdebugger.reader import CannotLoadSensor, CannotReadSensor
from subprocess import check_output

class Sensor(object):

    def __init__(self):
        # Do a read, if we can't find the binary, the reader throws an exception
        self.read()

    def read(self):
        try:
            line = check_output(["htu21dflib"])
        except Exception as err:
            raise CannotLoadSensor("Error: %s" % str(err))

        if line.startswith("#"):
            raise CannotReadSensor("Error: %s" % line[1:])

        temp, hum = line.split(" ")
        try:
            temp = float(temp)
            hum = float(hum)
        except ValueError:
            raise CannotReadSensor("Invalid data returned from sensor.")
            return None

        return (temp, hum)
