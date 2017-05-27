from math import sqrt, pow
from pykalman import KalmanFilter
from sleepdebugger.reader import Reader

class AccelerometerReader(Reader):

    def __init__(self, type, model):
        super(Reader, self).__init__(type, model)

        self.last_point = None
        self.points = []
        self.filename = filename

        self.mag_threshold2 = pow(config.ACCEL_MAG_THRESHOLD, 2)
        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        self.point = None
        self.covariance = [ [0.0], [0.0], [0.0] ]

    def _handle_point(self, raw_point):

        if not self.point:
            self.point = raw_point

        if config.ACCEL_FILTER:
            (self.point[0], self.covariance[0]) = self.kf.filter_update(self.point[0], self.covariance[0], raw_point[0])
            (self.point[1], self.covariance[1]) = self.kf.filter_update(self.point[1], self.covariance[1], raw_point[1])
            (self.point[2], self.covariance[2]) = self.kf.filter_update(self.point[2], self.covariance[2], raw_point[2])

            point = [self.point[0][0].data[0], self.point[1][0].data[0], self.point[2][0].data[0]]
        else:
            point = raw_point

        diff = ( abs(self.last_point[0] - point[0]), abs(self.last_point[1] - point[1]),  abs(self.last_point[2] - point[2]) )

        mag2 = pow(diff[0], 2) + pow(diff[1], 2) + pow(diff[2], 2)
        s = sqrt(mag2)
        if s > 2:
            print sqrt(mag2)
        if mag2 > self.mag_threshold2:
            self._notify(sqrt(mag2) - config.ACCEL_MAG_THRESHOLD)

        self.last_point = point

    def read(self):
        pt = list(self.sensor.read())
        if not self.last_point:
            self.last_point = pt
            continue
        
        self._handle_point(pt)
