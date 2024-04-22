#!/usr/bin/env python

from threading import Thread
import rospy
import time
from geometry_msgs.msg import Point, Pose, PoseStamped, PoseWithCovarianceStamped, Quaternion, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import ColorRGBA, Header, String, Int16
from visualization_msgs.msg import Marker, MarkerArray
from actionlib_msgs.msg import GoalStatusArray
from tf.transformations import euler_from_quaternion
from rah01_navigation import RA01Navigation
from rah01_people import RAH01People, RAH01PeopleStatus
from rah01_action import RAH01Action, RAH01ActionStatus
from enum import Enum

class RAH01Status(Enum):
    IDLE = 0
    WAITING = 1
    ACTIVE_GOAL = 2
    GOAL_REACHED = 3
    GOAL_FAILED = 4
    INTERACTING = 5

class RAH01:
    def __init__(self) -> None:
        
        #Inicialise class
        self._people = RAH01People()
        self._navigator = RA01Navigation()
        self._action = RAH01Action()
        
        #Inicialise People Detector Thread
        self._people_thread = Thread(target=self._people.loop, daemon=True)
        self._interact_with_people_thread = Thread(target=self._action.interact_with_person, daemon=True)
        
        #Inicialise variables
        self._camera_fov = 120
        self._max_angular_speed = 2
        self._max_lineal_speed = 2
        self._status: RAH01Status = RAH01Status.IDLE
        self._amcl_position = None
        self._scan_data = None
        
        #Inicialise ROS
        # rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.amcl_position_callback)
        rospy.Subscriber('/scan', LaserScan, self._people.update_scan)
        rospy.Subscriber('/scan', LaserScan, self._action.update_scan)
        rospy.Subscriber('/move_base_simple/goal', PoseStamped, self._navigator.update_goal)
        rospy.Subscriber('/rah01/status', Int16, self.status_callback)
        rospy.Subscriber('/move_base/status', GoalStatusArray, self._navigator.update_status)
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self._people.update_position)
        
        self._state_pub = rospy.Publisher('/rah01/status', Int16, queue_size=10)
        self._person_pub = rospy.Publisher('/rah01/person', Marker, queue_size=10)
        self._goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
        self._cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        rospy.init_node('rah01')
        self._rate = rospy.Rate(8)
        
    def init(self):
        # self._people.init()

        position1 = {"x": 10.104269455583406, "y": -7.725870621569122, "z": 0}
        orientation1 = {"x": 0, "y": 0, "z": 0.409504108152294, "w": -0.9123082732313647}

        position2 = {"x": -5.14830703734367, "y": 8.53444315436155, "z": 0}
        orientation2 = {"x": 0, "y": 0, "z": 0.39098444844205005, "w": 0.920397284370432}

        self._navigator.add_goal(position1, orientation1)
        self._navigator.add_goal(position2, orientation2)
        self._navigator.set_goal_publisher(self._goal_pub)

        self._action.set_people(self._people)
        self._action.set_cmd_vel_pub(self._cmd_vel_pub)
        self._action.waiting_movement()

        self._people.init()
        self._people.set_person_pub(self._person_pub)

        self._people_thread.start()

        self._status = RAH01Status.WAITING
    
    def status_callback(self, msg):
        self._status = RAH01Status(msg)
    
    def loop(self):
        while not rospy.is_shutdown():
            if self._status == RAH01Status.IDLE:
                return
            
            
            if self._status != RAH01Status.INTERACTING:
                self._action.update_status()
                self._status = RAH01Status(self._navigator.status)
            
            if self._people.status == RAH01PeopleStatus.PERSON_DETECTED and self._action.status == RAH01ActionStatus.READY:
                self._navigator.cancel_goal()
                self._interact_with_people_thread.start() 
                self._interact_with_people_thread = Thread(target=self._action.interact_with_person, daemon=True)
                print("PERSON DETECTED")
                self._status = RAH01Status.INTERACTING
            elif self._status == RAH01Status.WAITING or self._status == RAH01Status.GOAL_REACHED:
                print("NEXT GOAL")
                self._navigator.next_goal()
            elif self._status == RAH01Status.GOAL_FAILED:
                print("NEXT GOAL")
                self._navigator.next_goal()
            elif self._status == RAH01Status.INTERACTING:
                if self._action.status == RAH01ActionStatus.TIMEOUT:
                    self._status = RAH01Status.WAITING
            
            
            print("STATUS: ", self._status)
            
            time.sleep(0.1)
        
        
if __name__ == '__main__':
    try:
        rah01 = RAH01()
        rah01.init()
        rah01.loop()
    except rospy.ROSInterruptException:
        pass