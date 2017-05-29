from math import sqrt, pow
from sleepdebugger.reader import Reader

class RadarSensorReader(Reader):

    def __init__(self, type, model):
        super(RadarSensorReader, self).__init__(type, model)

        self.value = None

    def read(self):
        pt = int(self.sensor.read())
        if not self.value:
            self.value = pt

        if pt != self.value:
            self._save_data("radar", { 'radar' : pt })

        self.value = pt
