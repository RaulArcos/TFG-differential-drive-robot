#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# Global variable to store the latest lidar data
lidar_data = None

# Callback function to receive lidar data
def lidar_callback(data):
    global lidar_data
    lidar_data = data

# Main program
if __name__ == '__main__':
    rospy.init_node('lidar_wheel_control')
    rospy.Subscriber('/scan', LaserScan, lidar_callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if lidar_data is not None:
           
            ranges = lidar_data.ranges
            if min(ranges) < 0.2:
            
                cmd_vel = Twist()
                pub.publish(cmd_vel)
            else:
               
                cmd_vel = Twist()
                cmd_vel.linear.x = 5.0  
                pub.publish(cmd_vel)

        rate.sleep()