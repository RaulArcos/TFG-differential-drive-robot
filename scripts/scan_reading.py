#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def scan_callback(scan_data):
    # This function will be called whenever a new message is received on the "/scan" topic
    # You can process the laser scan data here
    # For simplicity, this example just prints the ranges from the laser scan
    print(len(scan_data.ranges))
    print("Laser Scan Ranges:", type(scan_data.ranges[0]), scan_data.ranges[0])

def main():
    # Initialize the ROS node with a unique name
    rospy.init_node('scan_listener', anonymous=True)

    # Subscribe to the "/scan" topic with the specified callback function
    rospy.Subscriber("/scan", LaserScan, scan_callback)

    # Spin to keep the script from exiting
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass