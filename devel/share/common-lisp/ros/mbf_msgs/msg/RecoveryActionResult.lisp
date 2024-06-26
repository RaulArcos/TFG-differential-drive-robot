; Auto-generated. Do not edit!


(cl:in-package mbf_msgs-msg)


;//! \htmlinclude RecoveryActionResult.msg.html

(cl:defclass <RecoveryActionResult> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (status
    :reader status
    :initarg :status
    :type actionlib_msgs-msg:GoalStatus
    :initform (cl:make-instance 'actionlib_msgs-msg:GoalStatus))
   (result
    :reader result
    :initarg :result
    :type mbf_msgs-msg:RecoveryResult
    :initform (cl:make-instance 'mbf_msgs-msg:RecoveryResult)))
)

(cl:defclass RecoveryActionResult (<RecoveryActionResult>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RecoveryActionResult>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RecoveryActionResult)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mbf_msgs-msg:<RecoveryActionResult> is deprecated: use mbf_msgs-msg:RecoveryActionResult instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <RecoveryActionResult>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-msg:header-val is deprecated.  Use mbf_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'status-val :lambda-list '(m))
(cl:defmethod status-val ((m <RecoveryActionResult>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-msg:status-val is deprecated.  Use mbf_msgs-msg:status instead.")
  (status m))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <RecoveryActionResult>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-msg:result-val is deprecated.  Use mbf_msgs-msg:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RecoveryActionResult>) ostream)
  "Serializes a message object of type '<RecoveryActionResult>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'status) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'result) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RecoveryActionResult>) istream)
  "Deserializes a message object of type '<RecoveryActionResult>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'status) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'result) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RecoveryActionResult>)))
  "Returns string type for a message object of type '<RecoveryActionResult>"
  "mbf_msgs/RecoveryActionResult")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RecoveryActionResult)))
  "Returns string type for a message object of type 'RecoveryActionResult"
  "mbf_msgs/RecoveryActionResult")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RecoveryActionResult>)))
  "Returns md5sum for a message object of type '<RecoveryActionResult>"
  "6ecfe7815ddc3f1bb9510b76f760072f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RecoveryActionResult)))
  "Returns md5sum for a message object of type 'RecoveryActionResult"
  "6ecfe7815ddc3f1bb9510b76f760072f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RecoveryActionResult>)))
  "Returns full string definition for message of type '<RecoveryActionResult>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%~%Header header~%actionlib_msgs/GoalStatus status~%RecoveryResult result~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: actionlib_msgs/GoalStatus~%GoalID goal_id~%uint8 status~%uint8 PENDING         = 0   # The goal has yet to be processed by the action server~%uint8 ACTIVE          = 1   # The goal is currently being processed by the action server~%uint8 PREEMPTED       = 2   # The goal received a cancel request after it started executing~%                            #   and has since completed its execution (Terminal State)~%uint8 SUCCEEDED       = 3   # The goal was achieved successfully by the action server (Terminal State)~%uint8 ABORTED         = 4   # The goal was aborted during execution by the action server due~%                            #    to some failure (Terminal State)~%uint8 REJECTED        = 5   # The goal was rejected by the action server without being processed,~%                            #    because the goal was unattainable or invalid (Terminal State)~%uint8 PREEMPTING      = 6   # The goal received a cancel request after it started executing~%                            #    and has not yet completed execution~%uint8 RECALLING       = 7   # The goal received a cancel request before it started executing,~%                            #    but the action server has not yet confirmed that the goal is canceled~%uint8 RECALLED        = 8   # The goal received a cancel request before it started executing~%                            #    and was successfully cancelled (Terminal State)~%uint8 LOST            = 9   # An action client can determine that a goal is LOST. This should not be~%                            #    sent over the wire by an action server~%~%#Allow for the user to associate a string with GoalStatus for debugging~%string text~%~%~%================================================================================~%MSG: actionlib_msgs/GoalID~%# The stamp should store the time at which this goal was requested.~%# It is used by an action server when it tries to preempt all~%# goals that were requested before a certain time~%time stamp~%~%# The id provides a way to associate feedback and~%# result message with specific goal requests. The id~%# specified must be unique.~%string id~%~%~%================================================================================~%MSG: mbf_msgs/RecoveryResult~%# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%~%# Predefined success codes:~%uint8 SUCCESS           = 0~%~%# Possible server codes:~%uint8 FAILURE           = 150~%uint8 CANCELED          = 151~%uint8 PAT_EXCEEDED      = 152~%uint8 TF_ERROR          = 153~%uint8 NOT_INITIALIZED   = 154~%uint8 INVALID_PLUGIN    = 155~%uint8 INTERNAL_ERROR    = 156~%uint8 STOPPED           = 157  # The recovery behaviour execution has been stopped rigorously~%uint8 IMPASSABLE        = 158  # Further execution would lead to a collision~%~%uint8 ERROR_RANGE_START = 150~%uint8 ERROR_RANGE_END   = 199~%~%# 171..199 are reserved as plugin specific errors:~%uint8 PLUGIN_ERROR_RANGE_START = 171~%uint8 PLUGIN_ERROR_RANGE_END   = 199~%~%uint32 outcome~%string message~%string used_plugin~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RecoveryActionResult)))
  "Returns full string definition for message of type 'RecoveryActionResult"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%~%Header header~%actionlib_msgs/GoalStatus status~%RecoveryResult result~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: actionlib_msgs/GoalStatus~%GoalID goal_id~%uint8 status~%uint8 PENDING         = 0   # The goal has yet to be processed by the action server~%uint8 ACTIVE          = 1   # The goal is currently being processed by the action server~%uint8 PREEMPTED       = 2   # The goal received a cancel request after it started executing~%                            #   and has since completed its execution (Terminal State)~%uint8 SUCCEEDED       = 3   # The goal was achieved successfully by the action server (Terminal State)~%uint8 ABORTED         = 4   # The goal was aborted during execution by the action server due~%                            #    to some failure (Terminal State)~%uint8 REJECTED        = 5   # The goal was rejected by the action server without being processed,~%                            #    because the goal was unattainable or invalid (Terminal State)~%uint8 PREEMPTING      = 6   # The goal received a cancel request after it started executing~%                            #    and has not yet completed execution~%uint8 RECALLING       = 7   # The goal received a cancel request before it started executing,~%                            #    but the action server has not yet confirmed that the goal is canceled~%uint8 RECALLED        = 8   # The goal received a cancel request before it started executing~%                            #    and was successfully cancelled (Terminal State)~%uint8 LOST            = 9   # An action client can determine that a goal is LOST. This should not be~%                            #    sent over the wire by an action server~%~%#Allow for the user to associate a string with GoalStatus for debugging~%string text~%~%~%================================================================================~%MSG: actionlib_msgs/GoalID~%# The stamp should store the time at which this goal was requested.~%# It is used by an action server when it tries to preempt all~%# goals that were requested before a certain time~%time stamp~%~%# The id provides a way to associate feedback and~%# result message with specific goal requests. The id~%# specified must be unique.~%string id~%~%~%================================================================================~%MSG: mbf_msgs/RecoveryResult~%# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%~%# Predefined success codes:~%uint8 SUCCESS           = 0~%~%# Possible server codes:~%uint8 FAILURE           = 150~%uint8 CANCELED          = 151~%uint8 PAT_EXCEEDED      = 152~%uint8 TF_ERROR          = 153~%uint8 NOT_INITIALIZED   = 154~%uint8 INVALID_PLUGIN    = 155~%uint8 INTERNAL_ERROR    = 156~%uint8 STOPPED           = 157  # The recovery behaviour execution has been stopped rigorously~%uint8 IMPASSABLE        = 158  # Further execution would lead to a collision~%~%uint8 ERROR_RANGE_START = 150~%uint8 ERROR_RANGE_END   = 199~%~%# 171..199 are reserved as plugin specific errors:~%uint8 PLUGIN_ERROR_RANGE_START = 171~%uint8 PLUGIN_ERROR_RANGE_END   = 199~%~%uint32 outcome~%string message~%string used_plugin~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RecoveryActionResult>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'status))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'result))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RecoveryActionResult>))
  "Converts a ROS message object to a list"
  (cl:list 'RecoveryActionResult
    (cl:cons ':header (header msg))
    (cl:cons ':status (status msg))
    (cl:cons ':result (result msg))
))
