from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib import SimpleActionClient
from geometry_msgs.msg import Pose, Point, Quaternion
import rospy
import time

class RA01Navigation:
    def __init__(self) -> None:   
        self._goal_pub = None 
        self._goals = [] #bool, goal
        self._goal_publisher = None
        self._status = 0
        self._fail_timeout = 5
        self._fail_time = 0
        self._failing = False
        self._last_seq = 20
        self._goal_timeout = 0
        self._client = SimpleActionClient('move_base', MoveBaseAction)
        self._current_goal = 0

    @property
    def status(self):
        
        if time.time() - self._goal_timeout > 60:
            self._goals[self._current_goal][0] = True
            return 3
        if self._status == 1:
            return 2  
        elif self._status == 3 or self._status == 6 or self._status == 2:
            return 3
        elif self._status == 0:
            return 1
        else:
            return self._status
    
    def add_goal(self, position, orientation):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"  # Assuming you're using the map frame
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(position["x"], position["y"], position["z"]),
                                  Quaternion(orientation["x"], orientation["y"],
                                             orientation["z"], orientation["w"]))
        self._goals.append([False, goal])
        print(self._goals)
    
    def next_goal(self):
        all_goals_sent = True
        for goal in self._goals:
            if not goal[0]:
                all_goals_sent = False
        if all_goals_sent:
            print("All goals have been reached, resetting...")
            for i in range(len(self._goals)):
                self._goals[i][0] = False
        
        for goal in self._goals:
            if not goal[0]:
                print(f"Sending goal")
                self.publish_goal(goal[1])
                self._current_goal = self._goals.index(goal)
                self._goal_timeout = time.time()
                return
    
    def cancel_goal(self):
        self._client.cancel_all_goals()

    def update_status(self, msg):
        if len(msg.status_list) == 0:
            return 1
        for status in msg.status_list:
            self._status = status.status
        if self._status == 4:
            if self._failing:
                if time.time() - self._fail_time > 5:
                    self._status = 4
                else:
                    self._status = 3
            else:
                self._fail_time = time.time()
                self._failing = True
        else:
            self._fail_time = 0
            self._failing = False
        
        if self._status == 3:
            self._goals[self._current_goal][0] = True
    
    def update_goal(self, msg):
        self._last_seq = msg.header.seq
    
    def publish_goal(self, goal):
        self._client.wait_for_server()
        self._client.send_goal(goal)

    def set_goal_publisher(self, goal_pubisher):
        self._goal_publisher = goal_pubisher
    
    
