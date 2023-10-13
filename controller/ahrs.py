import math

import numpy as np
from controller.quaternion import Quaternion


class MahonyAHRS:
    #sample_period = 1 / 256
    quaternion = Quaternion(1, 0, 0, 0)  # output quaternion describing the Earth relative to the sensor
    kp = 0  # algorithm proportional gain
    ki = 0  # algorithm integral gain
    _e_int = np.array([.0, .0, .0])  # integral error

    def __init__(self, quaternion=None, kp=None, ki=None):
        if quaternion is None:
            quaternion = Quaternion(1, 0, 0, 0)
        if kp is None:
            kp = 1
        if ki is None:
            ki = 0

        self.sample_period = None
        self.quaternion = quaternion  # output quaternion describing the Earth relative to the sensor
        self.kp = kp  # algorithm proportional gain
        self.ki = ki  # algorithm integral gain
        self._e_int = np.array([.0, .0, .0])  # integral error

    def normAcc(self, acc):
        norm = 0
        for val in acc:
            norm += val**2
        norm = math.sqrt(norm)
        return acc/norm

    def update(self, gyroscope, accelerometer, period):

        self.sample_period = period
        q = self.quaternion

        # Estimated vector of gravity
        v = [2 * (q[1] * q[3] - q[0] * q[2]),
             2 * (q[0] * q[1] + q[2] * q[3]),
             q[0] ** 2 - q[1] ** 2 - q[2] ** 2 + q[3] ** 2
             ]

        e = np.cross(accelerometer, v)
        if self.ki > 0:
            self._e_int += e * self.sample_period
        else:
            self._e_int = np.array([.0, .0, .0])
        #Combination of Gyro data and Acc data (kp is deciding how significant is accdata)
        gyroscope = gyroscope + self.kp * e + self.ki * self._e_int

        q1 = q[0]
        q2 = q[1]
        q3 = q[2]
        q4 = q[3]
        gx = gyroscope[0]
        gy = gyroscope[1]
        gz = gyroscope[2]

        pa = q2
        pb = q3
        pc = q4
        q1 = q1 + (-q2 * gx - q3 * gy - q4 * gz) * (0.5 * self.sample_period)
        q2 = pa + (q1 * gx + pb * gz - pc * gy) * (0.5 * self.sample_period)
        q3 = pb + (q1 * gy - pa * gz + pc * gx) * (0.5 * self.sample_period)
        q4 = pc + (q1 * gz + pa * gy - pb * gx) * (0.5 * self.sample_period)

        self.quaternion.q = np.array([q1, q2, q3, q4])
        self.quaternion.q = self.quaternion.norm()
