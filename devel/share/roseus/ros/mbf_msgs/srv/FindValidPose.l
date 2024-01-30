;; Auto-generated. Do not edit!


(when (boundp 'mbf_msgs::FindValidPose)
  (if (not (find-package "MBF_MSGS"))
    (make-package "MBF_MSGS"))
  (shadow 'FindValidPose (find-package "MBF_MSGS")))
(unless (find-package "MBF_MSGS::FINDVALIDPOSE")
  (make-package "MBF_MSGS::FINDVALIDPOSE"))
(unless (find-package "MBF_MSGS::FINDVALIDPOSEREQUEST")
  (make-package "MBF_MSGS::FINDVALIDPOSEREQUEST"))
(unless (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE")
  (make-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))

(in-package "ROS")

(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(intern "*LOCAL_COSTMAP*" (find-package "MBF_MSGS::FINDVALIDPOSEREQUEST"))
(shadow '*LOCAL_COSTMAP* (find-package "MBF_MSGS::FINDVALIDPOSEREQUEST"))
(defconstant mbf_msgs::FindValidPoseRequest::*LOCAL_COSTMAP* 1)
(intern "*GLOBAL_COSTMAP*" (find-package "MBF_MSGS::FINDVALIDPOSEREQUEST"))
(shadow '*GLOBAL_COSTMAP* (find-package "MBF_MSGS::FINDVALIDPOSEREQUEST"))
(defconstant mbf_msgs::FindValidPoseRequest::*GLOBAL_COSTMAP* 2)

(defun mbf_msgs::FindValidPoseRequest-to-symbol (const)
  (cond
        ((= const 1) 'mbf_msgs::FindValidPoseRequest::*LOCAL_COSTMAP*)
        ((= const 2) 'mbf_msgs::FindValidPoseRequest::*GLOBAL_COSTMAP*)
        (t nil)))

(defclass mbf_msgs::FindValidPoseRequest
  :super ros::object
  :slots (_pose _safety_dist _dist_tolerance _angle_tolerance _costmap _current_pose _use_padded_fp ))

(defmethod mbf_msgs::FindValidPoseRequest
  (:init
   (&key
    ((:pose __pose) (instance geometry_msgs::PoseStamped :init))
    ((:safety_dist __safety_dist) 0.0)
    ((:dist_tolerance __dist_tolerance) 0.0)
    ((:angle_tolerance __angle_tolerance) 0.0)
    ((:costmap __costmap) 0)
    ((:current_pose __current_pose) nil)
    ((:use_padded_fp __use_padded_fp) nil)
    )
   (send-super :init)
   (setq _pose __pose)
   (setq _safety_dist (float __safety_dist))
   (setq _dist_tolerance (float __dist_tolerance))
   (setq _angle_tolerance (float __angle_tolerance))
   (setq _costmap (round __costmap))
   (setq _current_pose __current_pose)
   (setq _use_padded_fp __use_padded_fp)
   self)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:safety_dist
   (&optional __safety_dist)
   (if __safety_dist (setq _safety_dist __safety_dist)) _safety_dist)
  (:dist_tolerance
   (&optional __dist_tolerance)
   (if __dist_tolerance (setq _dist_tolerance __dist_tolerance)) _dist_tolerance)
  (:angle_tolerance
   (&optional __angle_tolerance)
   (if __angle_tolerance (setq _angle_tolerance __angle_tolerance)) _angle_tolerance)
  (:costmap
   (&optional __costmap)
   (if __costmap (setq _costmap __costmap)) _costmap)
  (:current_pose
   (&optional (__current_pose :null))
   (if (not (eq __current_pose :null)) (setq _current_pose __current_pose)) _current_pose)
  (:use_padded_fp
   (&optional (__use_padded_fp :null))
   (if (not (eq __use_padded_fp :null)) (setq _use_padded_fp __use_padded_fp)) _use_padded_fp)
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/PoseStamped _pose
    (send _pose :serialization-length)
    ;; float32 _safety_dist
    4
    ;; float32 _dist_tolerance
    4
    ;; float32 _angle_tolerance
    4
    ;; uint8 _costmap
    1
    ;; bool _current_pose
    1
    ;; bool _use_padded_fp
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/PoseStamped _pose
       (send _pose :serialize s)
     ;; float32 _safety_dist
       (sys::poke _safety_dist (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _dist_tolerance
       (sys::poke _dist_tolerance (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _angle_tolerance
       (sys::poke _angle_tolerance (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; uint8 _costmap
       (write-byte _costmap s)
     ;; bool _current_pose
       (if _current_pose (write-byte -1 s) (write-byte 0 s))
     ;; bool _use_padded_fp
       (if _use_padded_fp (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/PoseStamped _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;; float32 _safety_dist
     (setq _safety_dist (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _dist_tolerance
     (setq _dist_tolerance (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _angle_tolerance
     (setq _angle_tolerance (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; uint8 _costmap
     (setq _costmap (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; bool _current_pose
     (setq _current_pose (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _use_padded_fp
     (setq _use_padded_fp (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(intern "*FREE*" (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(shadow '*FREE* (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(defconstant mbf_msgs::FindValidPoseResponse::*FREE* 0)
(intern "*INSCRIBED*" (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(shadow '*INSCRIBED* (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(defconstant mbf_msgs::FindValidPoseResponse::*INSCRIBED* 1)
(intern "*LETHAL*" (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(shadow '*LETHAL* (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(defconstant mbf_msgs::FindValidPoseResponse::*LETHAL* 2)
(intern "*UNKNOWN*" (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(shadow '*UNKNOWN* (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(defconstant mbf_msgs::FindValidPoseResponse::*UNKNOWN* 3)
(intern "*OUTSIDE*" (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(shadow '*OUTSIDE* (find-package "MBF_MSGS::FINDVALIDPOSERESPONSE"))
(defconstant mbf_msgs::FindValidPoseResponse::*OUTSIDE* 4)

(defun mbf_msgs::FindValidPoseResponse-to-symbol (const)
  (cond
        ((= const 0) 'mbf_msgs::FindValidPoseResponse::*FREE*)
        ((= const 1) 'mbf_msgs::FindValidPoseResponse::*INSCRIBED*)
        ((= const 2) 'mbf_msgs::FindValidPoseResponse::*LETHAL*)
        ((= const 3) 'mbf_msgs::FindValidPoseResponse::*UNKNOWN*)
        ((= const 4) 'mbf_msgs::FindValidPoseResponse::*OUTSIDE*)
        (t nil)))

(defclass mbf_msgs::FindValidPoseResponse
  :super ros::object
  :slots (_state _cost _pose ))

(defmethod mbf_msgs::FindValidPoseResponse
  (:init
   (&key
    ((:state __state) 0)
    ((:cost __cost) 0)
    ((:pose __pose) (instance geometry_msgs::PoseStamped :init))
    )
   (send-super :init)
   (setq _state (round __state))
   (setq _cost (round __cost))
   (setq _pose __pose)
   self)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:cost
   (&optional __cost)
   (if __cost (setq _cost __cost)) _cost)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:serialization-length
   ()
   (+
    ;; uint8 _state
    1
    ;; uint32 _cost
    4
    ;; geometry_msgs/PoseStamped _pose
    (send _pose :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _state
       (write-byte _state s)
     ;; uint32 _cost
       (write-long _cost s)
     ;; geometry_msgs/PoseStamped _pose
       (send _pose :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _state
     (setq _state (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint32 _cost
     (setq _cost (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; geometry_msgs/PoseStamped _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;;
   self)
  )

(defclass mbf_msgs::FindValidPose
  :super ros::object
  :slots ())

(setf (get mbf_msgs::FindValidPose :md5sum-) "3b058229757805d017574e238e310b27")
(setf (get mbf_msgs::FindValidPose :datatype-) "mbf_msgs/FindValidPose")
(setf (get mbf_msgs::FindValidPose :request) mbf_msgs::FindValidPoseRequest)
(setf (get mbf_msgs::FindValidPose :response) mbf_msgs::FindValidPoseResponse)

(defmethod mbf_msgs::FindValidPoseRequest
  (:response () (instance mbf_msgs::FindValidPoseResponse :init)))

(setf (get mbf_msgs::FindValidPoseRequest :md5sum-) "3b058229757805d017574e238e310b27")
(setf (get mbf_msgs::FindValidPoseRequest :datatype-) "mbf_msgs/FindValidPoseRequest")
(setf (get mbf_msgs::FindValidPoseRequest :definition-)
      "# Find the closest free pose to the given one, within the given linear and angular tolerances.
#
# A pose is considered free if the robot footprint there is entirely inside the map and neither in
# collision nor unknown space.
#
# If no free pose can be found, but we find one partially in unknown space, or partially outside the map,
# we will return it and set state to the corresponding option (unknown space takes precedence).
# Otherwise state will be set to LETHAL.
#
# You can also instruct this service to use current robot's pose, instead of providing one.

uint8                      LOCAL_COSTMAP  = 1
uint8                      GLOBAL_COSTMAP = 2

geometry_msgs/PoseStamped  pose              # the starting pose from which we start the search
float32                    safety_dist       # minimum distance allowed to the closest obstacle
float32                    dist_tolerance    # maximum distance we can deviate from the given pose during the search
float32                    angle_tolerance   # maximum angle we can rotate the given pose during the search
uint8                      costmap           # costmap in which to check the pose
bool                       current_pose      # check current robot pose instead (ignores pose field)
bool                       use_padded_fp     # include footprint padding when checking cost; note that safety distance
                                             # will be measured from the padded footprint

================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
---
uint8                      FREE      =  0    # found pose is completely in traversable space
uint8                      INSCRIBED =  1    # found pose is partially in inscribed space
uint8                      LETHAL    =  2    # found pose is partially in collision
uint8                      UNKNOWN   =  3    # found pose is partially in unknown space
uint8                      OUTSIDE   =  4    # found pose is partially outside the map

uint8                      state             # found pose's state: FREE, INSCRIBED, LETHAL, UNKNOWN or OUTSIDE
uint32                     cost              # found pose's cost (sum of costs over all cells covered by the footprint)
geometry_msgs/PoseStamped  pose              # the pose found (filled only if state is not set to LETHAL)


================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
")

(setf (get mbf_msgs::FindValidPoseResponse :md5sum-) "3b058229757805d017574e238e310b27")
(setf (get mbf_msgs::FindValidPoseResponse :datatype-) "mbf_msgs/FindValidPoseResponse")
(setf (get mbf_msgs::FindValidPoseResponse :definition-)
      "# Find the closest free pose to the given one, within the given linear and angular tolerances.
#
# A pose is considered free if the robot footprint there is entirely inside the map and neither in
# collision nor unknown space.
#
# If no free pose can be found, but we find one partially in unknown space, or partially outside the map,
# we will return it and set state to the corresponding option (unknown space takes precedence).
# Otherwise state will be set to LETHAL.
#
# You can also instruct this service to use current robot's pose, instead of providing one.

uint8                      LOCAL_COSTMAP  = 1
uint8                      GLOBAL_COSTMAP = 2

geometry_msgs/PoseStamped  pose              # the starting pose from which we start the search
float32                    safety_dist       # minimum distance allowed to the closest obstacle
float32                    dist_tolerance    # maximum distance we can deviate from the given pose during the search
float32                    angle_tolerance   # maximum angle we can rotate the given pose during the search
uint8                      costmap           # costmap in which to check the pose
bool                       current_pose      # check current robot pose instead (ignores pose field)
bool                       use_padded_fp     # include footprint padding when checking cost; note that safety distance
                                             # will be measured from the padded footprint

================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
---
uint8                      FREE      =  0    # found pose is completely in traversable space
uint8                      INSCRIBED =  1    # found pose is partially in inscribed space
uint8                      LETHAL    =  2    # found pose is partially in collision
uint8                      UNKNOWN   =  3    # found pose is partially in unknown space
uint8                      OUTSIDE   =  4    # found pose is partially outside the map

uint8                      state             # found pose's state: FREE, INSCRIBED, LETHAL, UNKNOWN or OUTSIDE
uint32                     cost              # found pose's cost (sum of costs over all cells covered by the footprint)
geometry_msgs/PoseStamped  pose              # the pose found (filled only if state is not set to LETHAL)


================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
")



(provide :mbf_msgs/FindValidPose "3b058229757805d017574e238e310b27")


