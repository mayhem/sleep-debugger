from math import sqrt, pow
from sleepdebugger.reader import Reader

class RadarSensorReader(Reader):

    report_interval = 10
    def __init__(self, type, model):
        super(RadarSensorReader, self).__init__(type, model)

        self.value = -1
        self.last_reported = 0


    def read(self):
        pt = self.sensor.read()
        if pt != self.value or (time() - self.last_reported) > self.report_interval:
            self._save_data("radar", { 'radar' : pt })
            self.last_reported = time()

        self.value = pt
