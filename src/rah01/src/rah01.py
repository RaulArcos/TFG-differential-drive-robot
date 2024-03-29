import math
import rospy
import time
from geometry_msgs.msg import Point, Pose, PoseStamped, PoseWithCovarianceStamped, Quaternion, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import ColorRGBA, Header, String, Int16
from visualization_msgs.msg import Marker, MarkerArray
from tf.transformations import euler_from_quaternion
from rah01_navigation import RA01Navigation
from rah01_people import RAH01People
from enum import Enum

class RAH01Status(Enum):
    IDLE = 0
    ACTIVE = 1
    ACTION = 2
    

class RAH01:
    def __init__(self) -> None:
        
        #Inicialise class
        self._people = RAH01People()
        self._navigator = RA01Navigation()
        
        #Inicialise variables
        self._camera_fov = 120
        self._max_angular_speed = 2
        self._max_lineal_speed = 2
        self._status: RAH01Status = RAH01Status.IDLE
        self._amcl_position = None
        self._scan_data = None
        
        #Inicialise ROS
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amcl_position_callback)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_callback)
        rospy.Subscriber('/rah01/status', Int16, self.status_callback)
        
        self._state_pub = rospy.Publisher('/rah01/status', Int16, queue_size=10)
        self._people_pub = rospy.Publisher('/rah01/people', MarkerArray, queue_size=10)
        self._goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
        self._cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        rospy.init_node('rah01')
        self._rate = rospy.Rate(8)
        
    def init(self):
        self._people.init()
        
    def amcl_position_callback(self, msg):
        self._navigator.update_position(msg)
    
    def scan_callback(self, msg):
        self._navigator.update_scan(msg)
    
    def goal_callback(self, msg):
        self._navigator.update_goal(msg)
    
    def status_callback(self, msg):
        self._status = RAH01Status(msg)
    
    def loop(self):
        while not rospy.is_shutdown():
            
            try:
                rospy.spin()
            except KeyboardInterrupt:
                pass    
            rospy.loginfo("finsihed!")
        
        
        
        