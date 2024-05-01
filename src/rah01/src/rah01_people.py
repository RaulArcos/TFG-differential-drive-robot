from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA, Header, String
from geometry_msgs.msg import Point, Pose, PoseStamped, PoseWithCovarianceStamped, Quaternion, Twist
from video_client import gstVideoClient
from RAH01Detector import detector
import rospy
import math
from enum import Enum

class RAH01PeopleStatus(Enum):
    NO_PEOPLE = 0
    PERSON_DETECTED = 1

class RAH01People:
    def __init__(self) -> None:
        self._detector = None
        self._video_client = gstVideoClient()
        self._scan_data = None
        self._nearest_person_position = None
        self._fov = 120
        self._robot_position = None
        self._robot_orientation = None
        self._person_array = None
        self._person_pub = None
        self._person_position = None
        self._person_angle_diference = 0
        self._person_distance = 0
        self._status: RAH01PeopleStatus = RAH01PeopleStatus.NO_PEOPLE
    
    def init(self):
        rospy.loginfo("Loading video client and detector...This may take up a few seconds!")
        self._video_client.init()
        rospy.loginfo("VideoClient Loaded!")
        self._detector = detector.RAH01Detector(model_path='/etc/rah01/models/yolov7-tiny.pt')
        rospy.loginfo("Detector Loaded!")

    @property
    def status(self):
        return self._status

    def get_person_angle_diference(self):
        return self._person_angle_diference
    
    def get_person_distance(self):
        return self._person_distance

    def set_person_pub(self, person_pub):
        self._person_pub = person_pub
    
    def update_scan(self, msg):
        self._scan_data = msg.ranges
    
    def update_position(self, msg):
        self._robot_position = msg.pose.pose.position
        self._robot_orientation = msg.pose.pose.orientation

    def get_nearest_target(self):
        return self._nearest_target
    
    def get_person_position(self):
        return self._person_position

    def calculateDistanceFromLaser(self, angle_init, angle_fin, angle_center):
        if self._scan_data is None:
            return None
        
        distance = 12
        if abs(angle_init - angle_fin) > 5:
            for angle in range(angle_center-3, angle_center+3, 1):
                distance = min(distance, self._scan_data[angle])
        if distance > 8:
            return None
        else:
            return distance
    
    def calculateAngleFromBoundingBox(self, box, half_width, fov):
        x1, _, x2, _ = box
        angle_start = ((x1 - half_width) / half_width) * (fov / 2.0)
        angle_end = ((x2 - half_width) / half_width) * (fov / 2.0)
        return angle_start, angle_end
    
    def quaternion_to_yaw(self, w, z):
        return math.atan2(2.0 * (w * z), 1.0 - 2.0 * (z ** 2))
    
    def person_position_in_map(self, d, theta, robot_pos, quaternion):
        theta_rad = math.radians(theta)
        w, z = quaternion.w, quaternion.z
        robot_orientation = self.quaternion_to_yaw(w, z)
        x_rel = d * math.cos(theta_rad)
        y_rel = d * math.sin(theta_rad)
        cos_phi = math.cos(robot_orientation)
        sin_phi = math.sin(robot_orientation)
        x_p = cos_phi * x_rel - sin_phi * y_rel + robot_pos.x
        y_p = sin_phi * x_rel + cos_phi * y_rel + robot_pos.y
        
        return (x_p, y_p)

    def loop(self):
        while(True):
            posible_targets = []
            _, frame = self._video_client.get_frame()
            if frame is not None and self._scan_data is not None:
                boxes, _ = self._detector.detectPersonOnly(frame, 416)
                for box in boxes:
                    angle_init, angle_fin = self.calculateAngleFromBoundingBox(box, frame.shape[1]/2, self._fov)
                    angle_center = (angle_init + angle_fin) / 2
                    angle_center= angle_center*-1
                    box_distance = self.calculateDistanceFromLaser(int(angle_init), int(angle_fin), int(angle_center))

                    if angle_center > 40 or angle_center < -40 or box_distance is None:
                        continue
    
                    posible_targets.append([box_distance, angle_center])
                
                if not len(posible_targets):
                    self._status = RAH01PeopleStatus.NO_PEOPLE
                    continue

                self._nearest_target = sorted(posible_targets, key=lambda x: x[0])

                if self._nearest_target[0][0] < 4:
                    self._status = RAH01PeopleStatus.PERSON_DETECTED
                else:
                    self._status = RAH01PeopleStatus.NO_PEOPLE
               
                self._person_distance = box_distance
                self._person_angle_diference = angle_center
                x_p, y_p = self.person_position_in_map(self._nearest_target[0][0], self._nearest_target[0][1], self._robot_position, self._robot_orientation)
                
                self._person_position = [x_p, y_p]

                person = Marker(
                    header=Header(stamp=rospy.Time.now(), frame_id="map"),
                    id=0,
                    type=Marker.SPHERE,
                    action=Marker.ADD,
                    pose=Pose(position=Point(x=x_p, y=y_p, z=0.0)),
                    scale=Point(x=0.2, y=0.2, z=0.1),
                    color=ColorRGBA(r=0.0, g=1.0, b=0.0, a=1.0),
                )

                self._person_pub.publish(person)