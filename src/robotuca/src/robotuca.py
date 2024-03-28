#!/usr/bin/env python
import rospy
import threading
from geometry_msgs.msg import Point, Pose, PoseStamped, PoseWithCovarianceStamped, Quaternion, Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import ColorRGBA, Header, String
from pid_controller import PIDController
from RobotUcaDetector import detector
from video_client import gstVideoClient

class RobotUca:
    def __init__(self) -> None:
        #Subscribers
        rospy.Subscriber('scan', LaserScan, self.laser_data_callback)
        rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.amcl_pose_callback)
        rospy.Subscriber('move_base_simple/goal', PoseStamped, self.goal_callback)
        
        #Publishers
        self._status_pub = rospy.Publisher('status', String, queue_size=1)
        self._goal_pub = rospy.Publisher("move_base_simple/goal", PoseStamped, queue_size=1)
        self._cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        
        #PID Controller
        self._pid_angular = PIDController(0.3, 0.000001, 0.0) #TODO: Ajustar
        self._pid_linear = PIDController(0.6, 0.000002, 0.0)
        
        #Detections
        self._detector = None
        self._video_client = gstVideoClient()
    
    def init(self):
        rospy.loginfo("Loading RobotUca, this may take a while...")
        detector.RobotUcaDetector(model_path='/etc/robotuca/models/yolov7-tiny.pt')
        rospy.loginfo("Detector Loaded!")
        self._video_client.init()
        rospy.loginfo("VideoClient Loaded!")
        rospy.init_node('people_follower')
        self._rate = rospy.Rate(8)
        rospy.loginfo("Robotuca Node Started!")
        
    
    def route_publisher(self):
    
    def loop(self):
        while not rospy.is_shutdown():
            
        
        
if __name__ == '__main__':
    try:
        robotuca = RobotUca()
        robotuca.init()
    except rospy.ROSInterruptException:
        pass