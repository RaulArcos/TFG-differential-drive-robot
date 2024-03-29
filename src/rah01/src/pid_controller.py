#!/usr/bin/env python
class PIDController:
    def __init__(self, Kp=0.01, Ki=0.0, Kd=0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0

    def calculate(self, error, delta_time):
        self.integral += error * delta_time
        derivative = (error - self.prev_error) / delta_time
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return output