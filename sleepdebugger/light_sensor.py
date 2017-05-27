from math import sqrt, pow
from pykalman import KalmanFilter
from sleepdebugger.reader import Reader, CannotLoadSensor, CannotReadSensor

class LightSensorReader(Reader):

    def __init__(self, type, model):
        super(Reader, self).__init__(type, model)

    def read(self):
        pt = int(self.sensor.read())
        print "light sensor: %d" % pt
        self._save_data(pt)
