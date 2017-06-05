from math import sqrt, pow
from pykalman import KalmanFilter
from sleepdebugger.reader import Reader, CannotLoadSensor, CannotReadSensor

class LightSensorReader(Reader):

    def __init__(self, type, model):
        super(LightSensorReader, self).__init__(type, model)

        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        self.point = None
        self.covariance = [ 0.0 ]

    def read(self):
        raw_point = [float(self.sensor.read())]
        if not self.point:
            self.point = raw_point

        (self.point, self.covariance) = self.kf.filter_update(self.point, self.covariance, raw_point)
        self._save_data("light", { 'light' : int(self.point[0]) })
