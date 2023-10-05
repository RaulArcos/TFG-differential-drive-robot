from __future__ import division
import pigpio
import time

class MotorTicks:

    def __init__(self):
        self.left = 0
        self.right = 0

class MockRobot:
    """Implements a mock robot that dutifully executes its wheel
    speed commands exactly.
    """

    def __init__(self):
        self.leftSpeed = 0
        self.newLeftSpeed = 0
        self.rightSpeed = 0
        self.newRightSpeed = 0
        self.leftTicks = 0
        self.rightTicks = 0
        self.minTicks = -32768
        self.maxTicks = 32767
        self.pi1=pigpio.pi()
        self.h1=self.pi1.serial_open("/dev/ttyS0",115200)
    def __del__(self):
		self.pi1.serial_close(self.h1)
		self.pi1.stop()
    def setSpeeds(self, left, right):
		print("vvvA")
		self.newLeftSpeed = left#left#/30000
		self.newRightSpeed = right#/30000
		print("vvvD")
		print(self.newLeftSpeed)
		print(self.newRightSpeed)
		#self.pi1.serial_write(self.h1,"v 1 "+str(float(self.newLeftSpeed))+"\r")
		#self.pi1.serial_write(self.h1,"v 0 "+str(float(-self.newRightSpeed))+"\r")
		#pi1.serial_close(h1)
		#pi1.stop()

    def updateRobot(self, dTime):
        self.leftTicks = self.addTicks(self.leftTicks, self.leftSpeed*dTime)
        self.rightTicks = self.addTicks(self.rightTicks, self.rightSpeed*dTime)
        self.leftSpeed = self.newLeftSpeed
        self.rightSpeed = self.newRightSpeed
        # print("Update")
        # print(self.leftTicks)
        # print(self.rightTicks)
        # print(self.leftSpeed)
        # print(self.rightSpeed)
        leftMotorSpeed=self.leftSpeed
        rightMotorSpeed=-self.rightSpeed
        self.pi1.serial_write(self.h1,"v 1 "+str(leftMotorSpeed)+"\r")
        self.pi1.serial_write(self.h1,"v 0 "+str(rightMotorSpeed)+"\r")
        
    def getTicks(self):
        ticks = MotorTicks()
        ticks.left = self.leftTicks
        ticks.right = self.rightTicks
        return ticks

    def addTicksInt(self, ticks):
        ticks
        if ticks > self.maxTicks:
            return int(ticks - self.maxTicks + self.minTicks)
        elif ticks < self.minTicks:
            return int(ticks - self.minTicks + self.maxTicks)
        else:
            return int(ticks)
            
    def addTicks(self, ticks, deltaTicks):
        ticks += deltaTicks
        if ticks > self.maxTicks:
            return int(ticks - self.maxTicks + self.minTicks)
        elif ticks < self.minTicks:
            return int(ticks - self.minTicks + self.maxTicks)
        else:
            return int(ticks)
