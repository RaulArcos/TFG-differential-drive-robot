#!/usr/bin/env python
import math
import rospy
from geometry_msgs.msg import Point, Pose, PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import ColorRGBA, Header, String
from visualization_msgs.msg import Marker, MarkerArray
from video_client import gstVideoClient
from RobotUcaDetector import detector

import time


class PeopleFollowerNode:
    def __init__(self) -> None:
        
        #Inicialise variables
        self._odom_position = None
        self._odom_orientation = None
        self._frame_width = None
        self._laser_data = None
        self._average_human_width = 0.55
        self._camera_fov = 120
        
        #ROS publishers and subscribers
        rospy.Subscriber('/odom', Odometry, self.odom_position_callback)
        rospy.Subscriber('/scan', LaserScan, self.laser_data_callback)
        self._pub = rospy.Publisher('people_follower_status', String, queue_size=10)
        self._people_pub = rospy.Publisher('people', MarkerArray, queue_size=10)
        self._goal_pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        
        #ROS init
        rospy.init_node('people_follower')
        rospy.loginfo("people_follower started!")
        self._rate = rospy.Rate(10)

        #Load detector and video client
        self._detector = detector.RobotUcaDetector(model_path='/etc/robotuca/models/yolov7-tiny.pt')
        rospy.loginfo("Detector Loaded!")
        self._video_client = gstVideoClient()
        self._video_client.init()
        rospy.loginfo("VideoClient Loaded!")

    def laser_data_callback(self, msg):
        self._laser_data = msg

    def odom_position_callback(self, msg):
        self._odom_position = msg.pose.pose.position
        self._odom_orientation = msg.pose.pose.orientation

    def calculateDistanceFromLaser(self, angle_init, angle_fin, angle_center):
        if self._laser_data is None:
            return None
        
        angle_center = int(angle_center)*-1                   
        if self._laser_data.ranges[angle_center] <= 8:
            return self._laser_data.ranges[angle_center]

        return None
    
    def calculate2Dpoint(self, angle_center, distance):
        robot_angle_rad = math.radians(self._odom_orientation.w)
        person_angle_rad = math.radians(angle_center*-1)
        
        x = self._odom_position.x + distance * math.cos(robot_angle_rad + person_angle_rad)
        y = self._odom_position.y + distance * math.sin(robot_angle_rad + person_angle_rad)
        
        return x, y
    
    def calculateDistanceFromBoundingBox(self, box):
        x1, _, x2, _ = box
        box_width = x2 - x1
        if self._frame_width is None:
            return None
        normalized_width = box_width / self._frame_width
        cm_dis = (normalized_width - 1.2) / -0.006
        m_dis = cm_dis / 100
        return m_dis
    
    def calculateAngleFromBoundingBox(self, box):
        x1, _, x2, _ = box
        image_width_center = self._frame_width / 2
        offset_init = x1 - image_width_center
        offset_fin = x2 - image_width_center
        return offset_init/self._frame_width * self._camera_fov, offset_fin/self._frame_width  * self._camera_fov
    
    def loop(self):
        while not rospy.is_shutdown():
            
            start_time = time.time()
            
            header = Header(stamp=rospy.Time.now(), frame_id="map")
            people_array = MarkerArray()
            _, frame = self._video_client.get_frame()
            
            if self._odom_position is None or frame is None:
                continue

            boxes, _ = self._detector.detectPersonOnly(frame)
            self._frame_width = frame.shape[1]
            
            idx = 0
            nearest_target = []
            
            for box in boxes:
                angle_init, angle_fin = self.calculateAngleFromBoundingBox(box)
                angle_center = (angle_init + angle_fin) / 2
                box_distance = self.calculateDistanceFromLaser(int(angle_init), int(angle_fin), int(angle_center))
                
                if box_distance is None:
                    continue
                
                person_x, person_y = self.calculate2Dpoint(int(angle_center), box_distance)
                
                person = Marker(
                    header=header,
                    id=idx,
                    type=Marker.SPHERE,
                    action=Marker.ADD,
                    pose=Pose(position=Point(x=person_x, y=person_y, z=0.0)),
                    scale=Point(x=0.2, y=0.2, z=0.1),
                    color=ColorRGBA(r=0.0, g=1.0, b=0.0, a=1.0),
                )
                
                nearest_target.append([box_distance, angle_center, person_x, person_y])
                people_array.markers.append(person)
                idx += 1
            
            self._people_pub.publish(people_array)
            nearest_target = sorted(nearest_target, key=lambda x: x[0])
            
            if len(nearest_target) == 0:
                continue
            
            distance, angle_center, person_x, person_y = nearest_target[0]
            
            goalpos = PoseStamped()
            goalpos.header.frame_id = "map" 
            
            if distance > 1.5:
                goalpos.pose.position.x = person_x + self._odom_position.x
                goalpos.pose.position.y = person_y + self._odom_position.y
            else:
                goalpos.pose.position.x = self._odom_position.x
                goalpos.pose.position.y = self._odom_position.y
                
            goalpos.pose.position.z = 0.0
            goalpos.pose.orientation.x = 0.0
            goalpos.pose.orientation.y = 0.0
            goalpos.pose.orientation.z = math.sin(angle_center / 2.0) + self._odom_orientation.z
            goalpos.pose.orientation.w = math.cos(angle_center / 2.0) + self._odom_orientation.w
            self._goal_pub.publish(goalpos)
            
            end_time = time.time()
            rospy.loginfo("Time: " + str(end_time - start_time))
            
        try:
            rospy.spin()
        except KeyboardInterrupt:
            pass    
        rospy.loginfo("finsihed!")

if __name__ == '__main__':
    try:
        PeopleFollowerNode().loop()
    except rospy.ROSInterruptException:
        pass
    
    

    