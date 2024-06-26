;; Auto-generated. Do not edit!


(when (boundp 'mbf_msgs::MoveBaseActionResult)
  (if (not (find-package "MBF_MSGS"))
    (make-package "MBF_MSGS"))
  (shadow 'MoveBaseActionResult (find-package "MBF_MSGS")))
(unless (find-package "MBF_MSGS::MOVEBASEACTIONRESULT")
  (make-package "MBF_MSGS::MOVEBASEACTIONRESULT"))

(in-package "ROS")
;;//! \htmlinclude MoveBaseActionResult.msg.html
(if (not (find-package "ACTIONLIB_MSGS"))
  (ros::roseus-add-msgs "actionlib_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass mbf_msgs::MoveBaseActionResult
  :super ros::object
  :slots (_header _status _result ))

(defmethod mbf_msgs::MoveBaseActionResult
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:status __status) (instance actionlib_msgs::GoalStatus :init))
    ((:result __result) (instance mbf_msgs::MoveBaseResult :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _status __status)
   (setq _result __result)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:status
   (&rest __status)
   (if (keywordp (car __status))
       (send* _status __status)
     (progn
       (if __status (setq _status (car __status)))
       _status)))
  (:result
   (&rest __result)
   (if (keywordp (car __result))
       (send* _result __result)
     (progn
       (if __result (setq _result (car __result)))
       _result)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; actionlib_msgs/GoalStatus _status
    (send _status :serialization-length)
    ;; mbf_msgs/MoveBaseResult _result
    (send _result :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; actionlib_msgs/GoalStatus _status
       (send _status :serialize s)
     ;; mbf_msgs/MoveBaseResult _result
       (send _result :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; actionlib_msgs/GoalStatus _status
     (send _status :deserialize buf ptr-) (incf ptr- (send _status :serialization-length))
   ;; mbf_msgs/MoveBaseResult _result
     (send _result :deserialize buf ptr-) (incf ptr- (send _result :serialization-length))
   ;;
   self)
  )

(setf (get mbf_msgs::MoveBaseActionResult :md5sum-) "84bf66bbfc0d4e67d5dca5ff8ec7479d")
(setf (get mbf_msgs::MoveBaseActionResult :datatype-) "mbf_msgs/MoveBaseActionResult")
(setf (get mbf_msgs::MoveBaseActionResult :definition-)
      "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======

Header header
actionlib_msgs/GoalStatus status
MoveBaseResult result

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
MSG: actionlib_msgs/GoalStatus
GoalID goal_id
uint8 status
uint8 PENDING         = 0   # The goal has yet to be processed by the action server
uint8 ACTIVE          = 1   # The goal is currently being processed by the action server
uint8 PREEMPTED       = 2   # The goal received a cancel request after it started executing
                            #   and has since completed its execution (Terminal State)
uint8 SUCCEEDED       = 3   # The goal was achieved successfully by the action server (Terminal State)
uint8 ABORTED         = 4   # The goal was aborted during execution by the action server due
                            #    to some failure (Terminal State)
uint8 REJECTED        = 5   # The goal was rejected by the action server without being processed,
                            #    because the goal was unattainable or invalid (Terminal State)
uint8 PREEMPTING      = 6   # The goal received a cancel request after it started executing
                            #    and has not yet completed execution
uint8 RECALLING       = 7   # The goal received a cancel request before it started executing,
                            #    but the action server has not yet confirmed that the goal is canceled
uint8 RECALLED        = 8   # The goal received a cancel request before it started executing
                            #    and was successfully cancelled (Terminal State)
uint8 LOST            = 9   # An action client can determine that a goal is LOST. This should not be
                            #    sent over the wire by an action server

#Allow for the user to associate a string with GoalStatus for debugging
string text


================================================================================
MSG: actionlib_msgs/GoalID
# The stamp should store the time at which this goal was requested.
# It is used by an action server when it tries to preempt all
# goals that were requested before a certain time
time stamp

# The id provides a way to associate feedback and
# result message with specific goal requests. The id
# specified must be unique.
string id


================================================================================
MSG: mbf_msgs/MoveBaseResult
# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======

# Predefined success codes:
uint8 SUCCESS           = 0

# Predefined general error codes:
uint8 FAILURE           = 10
uint8 CANCELED          = 11
uint8 COLLISION         = 12
uint8 OSCILLATION       = 13
uint8 START_BLOCKED     = 14
uint8 GOAL_BLOCKED      = 15
uint8 TF_ERROR          = 16
uint8 INTERNAL_ERROR    = 17

uint8 ERROR_RANGE_START = 10
uint8 ERROR_RANGE_END   = 49
# 21..49 are reserved for future general error codes

# Planning/controlling failures:
uint8 PLAN_FAILURE      = 50
# 51..99 are reserved as planner specific errors

uint8 CTRL_FAILURE      = 100
# 101..149 are reserved as controller specific errors

uint32 outcome
string message

# Configuration upon action completion
float32 dist_to_goal
float32 angle_to_goal
geometry_msgs/PoseStamped final_pose


================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

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



(provide :mbf_msgs/MoveBaseActionResult "84bf66bbfc0d4e67d5dca5ff8ec7479d")


