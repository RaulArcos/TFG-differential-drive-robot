from video_client import gstVideoClient
from RobotUcaDetector import detector
import rospy

class RAH01People:
    def __init__(self) -> None:
        self._detector = None
        self._video_client = gstVideoClient()
    
    def init(self):
        rospy.loginfo("Loading video client and detector...This may take up a few seconds!")
        self._video_client.init()
        rospy.loginfo("VideoClient Loaded!")
        self._detector = detector.RobotUcaDetector(model_path='/etc/robotuca/models/yolov7-tiny.pt')
        rospy.loginfo("Detector Loaded!")