import numpy as np
import serial
import time
from controller.ahrs import MahonyAHRS

PI = 3.14159265
b = np.array([0.003305, -0.017726, -0.134052])
A = np.array([[0.996394, 0.000177, 0.002939],
            [0.000177, 0.997292, 0.001338],
            [-0.002939, 0.001338, 0.983761]])

class Controller:
    def __init__(self):
        self.serialPort = serial.Serial(port="COM3", baudrate=19200,
                                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        self.quater = MahonyAHRS()
        self.ActualTime = time.time()
        self.LastTime = 0
        self.serialPort.flushInput()
        self.serialPort.readline()
        self.serialPort.readline()

    
    def getRotations(self):
        self.LastTime = self.ActualTime
        self.ActualTime = time.time()
        ElapsedTime = self.ActualTime - self.LastTime

        data = self.serialPort.readline()
        try:
            data = data.decode('UTF-8')
            data = data.split(',')
            data[5] = data[5].rstrip()
            accData = data[0:3]
            calibData = np.zeros(3)
            for i in range(len(accData)):
                accData[i] = float(accData[i])
            gyroData = data[3:6]
            for i in range(len(gyroData)):
                gyroData[i] = float(gyroData[i])
        except:
            print("Error occurred while reading data")
            return 0, 0, 0

        accData = np.array(accData)
        calibData = A @ (accData - b)
        accData = calibData

        gyroData = np.array(gyroData)
        gyroData /= np.array([180/PI])
        roll, pitch, yaw = self.quater.quaternion.to_euler_angles()
        self.quater.update(gyroData, accData, ElapsedTime)
        return roll, pitch, yaw        

