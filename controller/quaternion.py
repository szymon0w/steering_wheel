import numpy as np
import numbers
import math


class Quaternion:

    def __init__(self, w_or_q, x=None, y=None, z=None):

        self._q = np.array([1.0, .0, .0, .0])
        if x is not None and y is not None and z is not None:
            w = w_or_q
            q = np.array([float(w), float(x), float(y), float(z)])
        elif isinstance(w_or_q, Quaternion):
            q = np.array(w_or_q.q)
        else:
            q = np.array(w_or_q)
            if len(q) != 4:
                raise ValueError("Expecting a 4-element array or w x y z as parameters")

        self._set_q(q)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            w = self._q[0] * other._q[0] - self._q[1] * other._q[1] - self._q[2] * other._q[2] - self._q[3] * other._q[
                3]
            x = self._q[0] * other._q[1] + self._q[1] * other._q[0] + self._q[2] * other._q[3] - self._q[3] * other._q[
                2]
            y = self._q[0] * other._q[2] - self._q[1] * other._q[3] + self._q[2] * other._q[0] + self._q[3] * other._q[
                1]
            z = self._q[0] * other._q[3] + self._q[1] * other._q[2] - self._q[2] * other._q[1] + self._q[3] * other._q[
                0]

            return Quaternion(w, x, y, z)
        elif isinstance(other, numbers.Number):
            q = self._q * other
            return Quaternion(q)

    def __add__(self, other):
        if not isinstance(other, Quaternion):
            if len(other) != 4:
                raise TypeError("Quaternions must be added to other quaternions or a 4-element array")
            q = self.q + other
        else:
            q = self.q + other.q

        return Quaternion(q)

    def to_euler_angles(self):
        w = self.q[0]
        x = self.q[1]
        y = self.q[2]
        z = self.q[3]

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        return roll_x, yaw_z, pitch_y

    def size(self):
        return np.sqrt(self.q[0] ** 2 + self.q[1] ** 2 + self.q[2] ** 2 + self.q[3] ** 2)

    def norm(self):
        return self._q / self.size()

    def _set_q(self, q):
        self._q = q

    def _get_q(self):
        return self._q

    q = property(_get_q, _set_q)

    def __getitem__(self, item):
        return self._q[item]

    def __array__(self):
        return self._q

    def __str__(self):
        return str(self.__array__().tolist())