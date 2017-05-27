#!/usr/bin/env python
import os
import sys
import json
from time import sleep
from influxdb import InfluxDBClient
import sleepdebugger.config as config

class CannotLoadSensor(Exception):
    pass

class CannotReadSensor(Exception):
    pass

class Reader(object):

    def __init__(self, type, model):
        self.influx = InfluxDBClient(config.INFLUX_HOST, config.INFLUX_PORT, config.INFLUX_USER, config.INFLUX_PASSWd, config.INFLUX_DB)
        self.sensor = None

        self._load_sensor(type, model)

    def _load_sensor(self, type, model):
        module = "sleepdebugger.%ss.%s" % (type, model)
        try:
            mod = __import__(module)
        except as err:
            raise CannotLoadSensor

        self.sensor = mod.Sensor()

    def _save_data(self, data):
        json_body = [
            {
                "measurement": config.INFLUX_DB,
                "tags": 
                {
                    "sleeper": config.SLEEPER
                },
                "fields": { }
            }
        ]
        for k in data:
            json_body['fields'][k] = data[k]

        #self.influx.write_points(json_body)

    @abstractmethod
    def read(self):
        pass
