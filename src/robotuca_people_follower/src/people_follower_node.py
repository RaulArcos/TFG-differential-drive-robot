#!/usr/bin/env python

import rospy
from video_client import gstVideoClient
from RobotUcaDetector import detector
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import math

class PeopleFollower:
    def __init__(self) -> None:
        rospy.init_node('people_follower')
        rospy.loginfo("people_follower started!")
        self._pub = rospy.Publisher('people_follower_status', String, queue_size=10)
        self._odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_position_callback)
        self._laser_data = rospy.Subscriber('/laser/scan', LaserScan, self.laser_data_callback)
        self._goal_pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        self._rate = rospy.Rate(10)

        self._detector = detector.RobotUcaDetector(model_path='/etc/robotuca/models/yolov7-tiny.pt')
        rospy.loginfo("Detector Loaded!")
        self._video_client = gstVideoClient()
        self._video_client.init()
        rospy.loginfo("VideoClient Loaded!")

        self._odom_position = None
        self._frame_width = None
        self._average_human_width = 0.55
        self._camera_fov = 55

    def laser_data_callback(self, msg):
        self._laser_data = msg

    def odom_position_callback(self, msg):
        self._odom_position = msg.pose.pose.position

    def calculateDistanceFromLaser(self):
        return None
    
    def calculateDistanceFromBoundingBox(self, box):
        x1, y1, x2, y2 = box
        box_width = x2 - x1
        if self._frame_width is None:
            return None
        normalized_width = box_width / self._frame_width
        cm_dis = (normalized_width - 1.2) / -0.006
        m_dis = cm_dis / 100
        return m_dis
    
    def calculateAngleFromBoundingBox(self, box):
        x1, y1, x2, y2 = box
        box_width = x2 - x1
        box_center = ((x2 + x1) / 2, (y2 + y1) / 2)
        image_width_center = self._frame_width / 2
        camera_fov_horizontal_rad = math.radians(self._camera_fov)

        offset = box_center[0] - image_width_center

        return math.atan(offset / (self._frame_width / 2) * math.tan(math.radians(self._camera_fov) / 2))
    
    def loop(self):
        while not rospy.is_shutdown():

            nframe, frame = self._video_client.get_frame()
            if frame is None:
                continue

            boxes, scores = self._detector.detectPersonOnly(frame)
            self._frame_width = frame.shape[1]
            biggest_box = None

            for i in range(len(boxes)):
                if biggest_box is None:
                    biggest_box = boxes[i]
                else:
                    if scores[i] > 60:
                        if (boxes[i][2] - boxes[i][0]) * (boxes[i][3] - boxes[i][1]) > (biggest_box[2] - biggest_box[0]) * (biggest_box[3] - biggest_box[1]):
                            biggest_box = boxes[i]

            if biggest_box is None:
                continue

            m_dis = self.calculateDistanceFromBoundingBox(biggest_box)
            horizontal_angle_transformation = self.calculateAngleFromBoundingBox(biggest_box)
            
            if m_dis is None or horizontal_angle_transformation is None:
                continue

            # goalpos = self._odom_position

            goalpos = PoseStamped()
            goalpos.header.frame_id = "map" 
            goalpos.pose.position.x = 0.0
            goalpos.pose.position.y = 0.0
            goalpos.pose.position.z = 0.0

            goalpos.pose.orientation.x = 0.0
            goalpos.pose.orientation.y = 0.0
            goalpos.pose.orientation.z = 0.0
            goalpos.pose.orientation.w = 0.0

            if m_dis < 1:
                m_dis = 0

            
            robot_orientation = 2.0 * math.atan2(goalpos.pose.orientation.z, goalpos.pose.orientation.w)

            goalpos.header.frame_id = "map" 
            goalpos.pose.position.x += m_dis * math.cos(robot_orientation + horizontal_angle_transformation)
            goalpos.pose.position.y += m_dis * math.sin(robot_orientation + horizontal_angle_transformation)
            goalpos.pose.position.z = 0.0

            goalpos.pose.orientation.x = 0.0
            goalpos.pose.orientation.y = 0.0
            goalpos.pose.orientation.z += math.sin(horizontal_angle_transformation / 2.0)
            goalpos.pose.orientation.w += math.cos(horizontal_angle_transformation / 2.0)

            self._goal_pub.publish(goalpos)

        try:
            rospy.spin()
        except KeyboardInterrupt:
            pass    
        rospy.loginfo("finsihed!")

if __name__ == '__main__':
    try:
        PeopleFollower().loop()
    except rospy.ROSInterruptException:
        pass
    
    

    