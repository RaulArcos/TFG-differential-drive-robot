#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

# Global variables to store the latest lidar data
lidar_data = None
lidar_angles = None

# Callback function to receive lidar data
def lidar_callback(data):
    global lidar_data, lidar_angles
    lidar_data = data
    lidar_angles = [(data.angle_min + i * data.angle_increment) for i in range(len(data.ranges))]

# Main program
if __name__ == '__main__':
    rospy.init_node('lidar_wheel_control')

    # Subscribe to the /scan topic
    rospy.Subscriber('/scan', LaserScan, lidar_callback)

    # Create a publisher for sending speed commands to the wheels
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Set the loop rate (in Hz)
    rate = rospy.Rate(10)

    # Main loop
    while not rospy.is_shutdown():
        if lidar_data is not None:
            # Read the range values from the lidar data
            ranges = lidar_data.ranges

            # Check if the lidar detects an object within 20cm
            if min(ranges) < 0.2:
                # Stop the wheels
                cmd_vel = Twist()
                pub.publish(cmd_vel)

                # Determine the index of the minimum range value
                min_range_index = ranges.index(min(ranges))

                # Calculate the angle corresponding to the minimum range
                min_range_angle = lidar_angles[min_range_index]

                # Print the direction of the wall
                if min_range_angle < 0:
                    print("Pared detrás! Girando...")
                    # Move the wheels in the opposite direction (right)
                    cmd_vel = Twist()
                    cmd_vel.angular.z = -1.0  # Set the desired angular velocity
                    pub.publish(cmd_vel)
                else:
                    print("Pared enfrente! Girando...")
                    # Move the wheels in the opposite direction (left)
                    cmd_vel = Twist()
                    cmd_vel.angular.z = 1.0  # Set the desired angular velocity
                    pub.publish(cmd_vel)
                print(min_range_angle)
            else:
                # Move the wheels forward
                cmd_vel = Twist()
                cmd_vel.linear.x = 3.0  # Set the desired linear velocity
                pub.publish(cmd_vel)

        # Sleep to maintain the loop rate
        rate.sleep()