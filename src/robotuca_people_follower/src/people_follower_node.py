#!/usr/bin/env python
import math
import rospy
from geometry_msgs.msg import Point, Pose, PoseStamped, PoseWithCovarianceStamped, Quaternion, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import ColorRGBA, Header, String
from visualization_msgs.msg import Marker, MarkerArray
from video_client import gstVideoClient
from RobotUcaDetector import detector
import time
from tf.transformations import euler_from_quaternion
from robotuca_pid_controller import PIDController


class PeopleFollowerNode:
    def __init__(self) -> None:
        
        #Inicialise variables
        self._odom_position = None
        self._odom_orientation = None
        self._frame_width = None
        self._laser_data = None
        self._average_human_width = 0.55
        self._camera_fov = 120
        self._max_angular_speed = 2
        self._min_angular_speed = 0
        self._max_lineal_speed = 2
        self._min_lineal_speed = 0

        self._last_iteration_time = time.time()
        self._pid_angular = PIDController(0.3, 0.000001, 0.0)
        self._pid_linear = PIDController(0.6, 0.000002, 0.0)
        
        #ROS publishers and subscribers
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.odom_position_callback)
        rospy.Subscriber('/scan', LaserScan, self.laser_data_callback)
        self._pub = rospy.Publisher('people_follower_status', String, queue_size=10)
        self._people_pub = rospy.Publisher('people', MarkerArray, queue_size=10)
        self._goal_pub = rospy.Publisher("move_base_simple/goal", PoseStamped, queue_size=1)
        self._cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        
        #ROS init
        rospy.init_node('people_follower')
        rospy.loginfo("people_follower started!")
        self._rate = rospy.Rate(8)

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
        
        distance = 12
        if abs(angle_init - angle_fin) > 5:
            for angle in range(angle_center-3, angle_center+3, 1):
                distance = min(distance, self._laser_data.ranges[angle])
        if distance == 12:
            return None
        else:
            return distance
    
    def calculate2Dpoint(self, angle_center, distance):
        _, _, yaw = self.euler_from_quaternion(self._odom_orientation)  # Get yaw from quaternion
        person_angle_rad = math.radians(angle_center)
        
        # Adjust calculation to use yaw for robot's orientation
        x = self._odom_position.x + distance * math.cos(yaw + person_angle_rad)
        y = self._odom_position.y + distance * math.sin(yaw + person_angle_rad)
        
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
        angle_start = ((x1 - (self._frame_width / 2.0)) / (self._frame_width / 2.0)) * (self._camera_fov / 2.0)
        angle_end = ((x2 - (self._frame_width / 2.0)) / (self._frame_width / 2.0)) * (self._camera_fov / 2.0)
        return angle_start, angle_end

    def euler_from_quaternion(self, orientation):
        q = [orientation.x, orientation.y, orientation.z, orientation.w]
        euler = euler_from_quaternion(q)
        return euler 
    
    def loop(self):
        while not rospy.is_shutdown():
            
            start_time = time.time()

            header = Header(stamp=rospy.Time.now(), frame_id="map")
            people_array = MarkerArray()
            _, frame = self._video_client.get_frame()

            if frame is None:
                continue

            boxes, _ = self._detector.detectPersonOnly(frame)
            self._frame_width = frame.shape[1]
            
            idx = 0
            nearest_target = []
            
            for box in boxes:
                angle_init, angle_fin = self.calculateAngleFromBoundingBox(box)
                angle_center = (angle_init + angle_fin) / 2
                angle_center= angle_center*-1
                box_distance = self.calculateDistanceFromLaser(int(angle_init), int(angle_fin), int(angle_center))

                if angle_center > 40 or angle_center < -40 or box_distance is None:
                    continue
                
                # person_x, person_y = self.calculate2Dpoint(angle_center,  box_distance)
                
            #     person = Marker(
            #         header=header,
            #         id=idx,
            #         type=Marker.SPHERE,
            #         action=Marker.ADD,
            #         pose=Pose(position=Point(x=person_x, y=person_y, z=0.0)),
            #         scale=Point(x=0.2, y=0.2, z=0.1),
            #         color=ColorRGBA(r=0.0, g=1.0, b=0.0, a=1.0),
            #     )
                person_x = 0
                person_y = 0
                nearest_target.append([box_distance, angle_center, person_x, person_y])
            #     people_array.markers.append(person)
            #     idx += 1

            # self._people_pub.publish(people_array)
            nearest_target = sorted(nearest_target, key=lambda x: x[0])

            vel_msg = Twist()
            
            if len(nearest_target) == 0:
                vel_msg.linear.x = 0  # forward
                vel_msg.linear.y = 0    # no sideways
                vel_msg.linear.z = 0    # no up/down

                # Set angular velocity (rad/s)
                vel_msg.angular.x = 0   # no roll
                vel_msg.angular.y = 0   # no pitch
                vel_msg.angular.z = 0 # rotate clockwise
                self._cmd_vel_pub.publish(vel_msg)
                continue
            
            distance, angle_center, person_x, person_y = nearest_target[0]
            angular_error = angle_center/5
            
            lineal_error = (distance - 1) if distance > 1 else 0

            angular_velocity = self._pid_angular.calculate(angular_error, time.time() - self._last_iteration_time)
            linear_velocity = self._pid_linear.calculate(lineal_error, time.time() - self._last_iteration_time)

            print("\n\n\n\n\n\n\n\nANGULAR ERROR: ", float(angular_error), float(angular_velocity))
            print("LINEAL ERROR: ", float(lineal_error), float(linear_velocity))
            print(distance)

            if linear_velocity > self._max_lineal_speed and linear_velocity> 0:
                linear_velocity = self._max_lineal_speed
            elif linear_velocity < self._max_lineal_speed and linear_velocity < 0:
                linear_velocity = self._max_lineal_speed
            
            

            print(linear_velocity, angular_velocity)

            vel_msg = Twist()
            vel_msg.linear.x = 0

            if distance < 8 and distance > 1.5:
                vel_msg.linear.x = linear_velocity 

            for angle in range(-40, 40, 1):
                if  self._laser_data.ranges[angle] < 0.5:
                    vel_msg.linear.x = 0

            vel_msg.linear.y = 0   
            vel_msg.linear.z = 0 

            vel_msg.angular.x = 0 
            vel_msg.angular.y = 0 
            vel_msg.angular.z = angular_velocity

            self._cmd_vel_pub.publish(vel_msg)


            # if distance > 5:
            #     continue
            
            # distance = distance - 0.5

            # goalpos = PoseStamped()
            # goalpos.header.frame_id = "map" 
            
            # if distance > 1.5:
            #     goalpos.pose.position.x = person_x
            #     goalpos.pose.position.y = person_y 
            # else:
            #     goalpos.pose.position.x = self._odom_position.x
            #     goalpos.pose.position.y = self._odom_position.y
                
            # goalpos.pose.position.z = 0.0
            # goalpos.pose.orientation.x = 0.0
            # goalpos.pose.orientation.y = 0.0
            # goalpos.pose.orientation.z = self._odom_orientation.z
            # goalpos.pose.orientation.w = self._odom_orientation.w
            # self._goal_pub.publish(goalpos)
            
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
    
    

    