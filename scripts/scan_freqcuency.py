#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import time

class ScanFrequency:
    def __init__(self):
        self.prev_time = rospy.Time.now()
        self.sub = rospy.Subscriber("/scan", LaserScan, self.callback)
        self.message_count = 0

    def callback(self, data):
        current_time = rospy.Time.now()
        self.message_count += 1

        # Calculate time difference in seconds
        time_diff = (current_time - self.prev_time).to_sec()
        if time_diff >= 1.0:  # Update frequency every second
            frequency = self.message_count / time_diff
            rospy.loginfo("Frequency: {:.2f} Hz".format(frequency))
            # Reset counters
            self.prev_time = current_time
            self.message_count = 0

if __name__ == '__main__':
    rospy.init_node('scan_frequency_monitor', anonymous=True)
    sf = ScanFrequency()
    rospy.spin()