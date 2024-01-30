; Auto-generated. Do not edit!


(cl:in-package mbf_msgs-srv)


;//! \htmlinclude FindValidPose-request.msg.html

(cl:defclass <FindValidPose-request> (roslisp-msg-protocol:ros-message)
  ((pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:PoseStamped
    :initform (cl:make-instance 'geometry_msgs-msg:PoseStamped))
   (safety_dist
    :reader safety_dist
    :initarg :safety_dist
    :type cl:float
    :initform 0.0)
   (dist_tolerance
    :reader dist_tolerance
    :initarg :dist_tolerance
    :type cl:float
    :initform 0.0)
   (angle_tolerance
    :reader angle_tolerance
    :initarg :angle_tolerance
    :type cl:float
    :initform 0.0)
   (costmap
    :reader costmap
    :initarg :costmap
    :type cl:fixnum
    :initform 0)
   (current_pose
    :reader current_pose
    :initarg :current_pose
    :type cl:boolean
    :initform cl:nil)
   (use_padded_fp
    :reader use_padded_fp
    :initarg :use_padded_fp
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass FindValidPose-request (<FindValidPose-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FindValidPose-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FindValidPose-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mbf_msgs-srv:<FindValidPose-request> is deprecated: use mbf_msgs-srv:FindValidPose-request instead.")))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <FindValidPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:pose-val is deprecated.  Use mbf_msgs-srv:pose instead.")
  (pose m))

(cl:ensure-generic-function 'safety_dist-val :lambda-list '(m))
(cl:defmethod safety_dist-val ((m <FindValidPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:safety_dist-val is deprecated.  Use mbf_msgs-srv:safety_dist instead.")
  (safety_dist m))

(cl:ensure-generic-function 'dist_tolerance-val :lambda-list '(m))
(cl:defmethod dist_tolerance-val ((m <FindValidPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:dist_tolerance-val is deprecated.  Use mbf_msgs-srv:dist_tolerance instead.")
  (dist_tolerance m))

(cl:ensure-generic-function 'angle_tolerance-val :lambda-list '(m))
(cl:defmethod angle_tolerance-val ((m <FindValidPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:angle_tolerance-val is deprecated.  Use mbf_msgs-srv:angle_tolerance instead.")
  (angle_tolerance m))

(cl:ensure-generic-function 'costmap-val :lambda-list '(m))
(cl:defmethod costmap-val ((m <FindValidPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:costmap-val is deprecated.  Use mbf_msgs-srv:costmap instead.")
  (costmap m))

(cl:ensure-generic-function 'current_pose-val :lambda-list '(m))
(cl:defmethod current_pose-val ((m <FindValidPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:current_pose-val is deprecated.  Use mbf_msgs-srv:current_pose instead.")
  (current_pose m))

(cl:ensure-generic-function 'use_padded_fp-val :lambda-list '(m))
(cl:defmethod use_padded_fp-val ((m <FindValidPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:use_padded_fp-val is deprecated.  Use mbf_msgs-srv:use_padded_fp instead.")
  (use_padded_fp m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<FindValidPose-request>)))
    "Constants for message type '<FindValidPose-request>"
  '((:LOCAL_COSTMAP . 1)
    (:GLOBAL_COSTMAP . 2))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'FindValidPose-request)))
    "Constants for message type 'FindValidPose-request"
  '((:LOCAL_COSTMAP . 1)
    (:GLOBAL_COSTMAP . 2))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FindValidPose-request>) ostream)
  "Serializes a message object of type '<FindValidPose-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'safety_dist))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'dist_tolerance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle_tolerance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'costmap)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'current_pose) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'use_padded_fp) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FindValidPose-request>) istream)
  "Deserializes a message object of type '<FindValidPose-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'safety_dist) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'dist_tolerance) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle_tolerance) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'costmap)) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'current_pose) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'use_padded_fp) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FindValidPose-request>)))
  "Returns string type for a service object of type '<FindValidPose-request>"
  "mbf_msgs/FindValidPoseRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FindValidPose-request)))
  "Returns string type for a service object of type 'FindValidPose-request"
  "mbf_msgs/FindValidPoseRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FindValidPose-request>)))
  "Returns md5sum for a message object of type '<FindValidPose-request>"
  "3b058229757805d017574e238e310b27")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FindValidPose-request)))
  "Returns md5sum for a message object of type 'FindValidPose-request"
  "3b058229757805d017574e238e310b27")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FindValidPose-request>)))
  "Returns full string definition for message of type '<FindValidPose-request>"
  (cl:format cl:nil "# Find the closest free pose to the given one, within the given linear and angular tolerances.~%#~%# A pose is considered free if the robot footprint there is entirely inside the map and neither in~%# collision nor unknown space.~%#~%# If no free pose can be found, but we find one partially in unknown space, or partially outside the map,~%# we will return it and set state to the corresponding option (unknown space takes precedence).~%# Otherwise state will be set to LETHAL.~%#~%# You can also instruct this service to use current robot's pose, instead of providing one.~%~%uint8                      LOCAL_COSTMAP  = 1~%uint8                      GLOBAL_COSTMAP = 2~%~%geometry_msgs/PoseStamped  pose              # the starting pose from which we start the search~%float32                    safety_dist       # minimum distance allowed to the closest obstacle~%float32                    dist_tolerance    # maximum distance we can deviate from the given pose during the search~%float32                    angle_tolerance   # maximum angle we can rotate the given pose during the search~%uint8                      costmap           # costmap in which to check the pose~%bool                       current_pose      # check current robot pose instead (ignores pose field)~%bool                       use_padded_fp     # include footprint padding when checking cost; note that safety distance~%                                             # will be measured from the padded footprint~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FindValidPose-request)))
  "Returns full string definition for message of type 'FindValidPose-request"
  (cl:format cl:nil "# Find the closest free pose to the given one, within the given linear and angular tolerances.~%#~%# A pose is considered free if the robot footprint there is entirely inside the map and neither in~%# collision nor unknown space.~%#~%# If no free pose can be found, but we find one partially in unknown space, or partially outside the map,~%# we will return it and set state to the corresponding option (unknown space takes precedence).~%# Otherwise state will be set to LETHAL.~%#~%# You can also instruct this service to use current robot's pose, instead of providing one.~%~%uint8                      LOCAL_COSTMAP  = 1~%uint8                      GLOBAL_COSTMAP = 2~%~%geometry_msgs/PoseStamped  pose              # the starting pose from which we start the search~%float32                    safety_dist       # minimum distance allowed to the closest obstacle~%float32                    dist_tolerance    # maximum distance we can deviate from the given pose during the search~%float32                    angle_tolerance   # maximum angle we can rotate the given pose during the search~%uint8                      costmap           # costmap in which to check the pose~%bool                       current_pose      # check current robot pose instead (ignores pose field)~%bool                       use_padded_fp     # include footprint padding when checking cost; note that safety distance~%                                             # will be measured from the padded footprint~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FindValidPose-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
     4
     4
     4
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FindValidPose-request>))
  "Converts a ROS message object to a list"
  (cl:list 'FindValidPose-request
    (cl:cons ':pose (pose msg))
    (cl:cons ':safety_dist (safety_dist msg))
    (cl:cons ':dist_tolerance (dist_tolerance msg))
    (cl:cons ':angle_tolerance (angle_tolerance msg))
    (cl:cons ':costmap (costmap msg))
    (cl:cons ':current_pose (current_pose msg))
    (cl:cons ':use_padded_fp (use_padded_fp msg))
))
;//! \htmlinclude FindValidPose-response.msg.html

(cl:defclass <FindValidPose-response> (roslisp-msg-protocol:ros-message)
  ((state
    :reader state
    :initarg :state
    :type cl:fixnum
    :initform 0)
   (cost
    :reader cost
    :initarg :cost
    :type cl:integer
    :initform 0)
   (pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:PoseStamped
    :initform (cl:make-instance 'geometry_msgs-msg:PoseStamped)))
)

(cl:defclass FindValidPose-response (<FindValidPose-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FindValidPose-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FindValidPose-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mbf_msgs-srv:<FindValidPose-response> is deprecated: use mbf_msgs-srv:FindValidPose-response instead.")))

(cl:ensure-generic-function 'state-val :lambda-list '(m))
(cl:defmethod state-val ((m <FindValidPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:state-val is deprecated.  Use mbf_msgs-srv:state instead.")
  (state m))

(cl:ensure-generic-function 'cost-val :lambda-list '(m))
(cl:defmethod cost-val ((m <FindValidPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:cost-val is deprecated.  Use mbf_msgs-srv:cost instead.")
  (cost m))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <FindValidPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mbf_msgs-srv:pose-val is deprecated.  Use mbf_msgs-srv:pose instead.")
  (pose m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<FindValidPose-response>)))
    "Constants for message type '<FindValidPose-response>"
  '((:FREE . 0)
    (:INSCRIBED . 1)
    (:LETHAL . 2)
    (:UNKNOWN . 3)
    (:OUTSIDE . 4))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'FindValidPose-response)))
    "Constants for message type 'FindValidPose-response"
  '((:FREE . 0)
    (:INSCRIBED . 1)
    (:LETHAL . 2)
    (:UNKNOWN . 3)
    (:OUTSIDE . 4))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FindValidPose-response>) ostream)
  "Serializes a message object of type '<FindValidPose-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'state)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'cost)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'cost)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'cost)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'cost)) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FindValidPose-response>) istream)
  "Deserializes a message object of type '<FindValidPose-response>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'state)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'cost)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'cost)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'cost)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'cost)) (cl:read-byte istream))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FindValidPose-response>)))
  "Returns string type for a service object of type '<FindValidPose-response>"
  "mbf_msgs/FindValidPoseResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FindValidPose-response)))
  "Returns string type for a service object of type 'FindValidPose-response"
  "mbf_msgs/FindValidPoseResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FindValidPose-response>)))
  "Returns md5sum for a message object of type '<FindValidPose-response>"
  "3b058229757805d017574e238e310b27")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FindValidPose-response)))
  "Returns md5sum for a message object of type 'FindValidPose-response"
  "3b058229757805d017574e238e310b27")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FindValidPose-response>)))
  "Returns full string definition for message of type '<FindValidPose-response>"
  (cl:format cl:nil "uint8                      FREE      =  0    # found pose is completely in traversable space~%uint8                      INSCRIBED =  1    # found pose is partially in inscribed space~%uint8                      LETHAL    =  2    # found pose is partially in collision~%uint8                      UNKNOWN   =  3    # found pose is partially in unknown space~%uint8                      OUTSIDE   =  4    # found pose is partially outside the map~%~%uint8                      state             # found pose's state: FREE, INSCRIBED, LETHAL, UNKNOWN or OUTSIDE~%uint32                     cost              # found pose's cost (sum of costs over all cells covered by the footprint)~%geometry_msgs/PoseStamped  pose              # the pose found (filled only if state is not set to LETHAL)~%~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FindValidPose-response)))
  "Returns full string definition for message of type 'FindValidPose-response"
  (cl:format cl:nil "uint8                      FREE      =  0    # found pose is completely in traversable space~%uint8                      INSCRIBED =  1    # found pose is partially in inscribed space~%uint8                      LETHAL    =  2    # found pose is partially in collision~%uint8                      UNKNOWN   =  3    # found pose is partially in unknown space~%uint8                      OUTSIDE   =  4    # found pose is partially outside the map~%~%uint8                      state             # found pose's state: FREE, INSCRIBED, LETHAL, UNKNOWN or OUTSIDE~%uint32                     cost              # found pose's cost (sum of costs over all cells covered by the footprint)~%geometry_msgs/PoseStamped  pose              # the pose found (filled only if state is not set to LETHAL)~%~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FindValidPose-response>))
  (cl:+ 0
     1
     4
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FindValidPose-response>))
  "Converts a ROS message object to a list"
  (cl:list 'FindValidPose-response
    (cl:cons ':state (state msg))
    (cl:cons ':cost (cost msg))
    (cl:cons ':pose (pose msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'FindValidPose)))
  'FindValidPose-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'FindValidPose)))
  'FindValidPose-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FindValidPose)))
  "Returns string type for a service object of type '<FindValidPose>"
  "mbf_msgs/FindValidPose")