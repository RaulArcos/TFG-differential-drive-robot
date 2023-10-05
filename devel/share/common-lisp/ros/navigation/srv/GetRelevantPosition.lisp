; Auto-generated. Do not edit!


(cl:in-package navigation-srv)


;//! \htmlinclude GetRelevantPosition-request.msg.html

(cl:defclass <GetRelevantPosition-request> (roslisp-msg-protocol:ros-message)
  ((relevantposition
    :reader relevantposition
    :initarg :relevantposition
    :type cl:integer
    :initform 0))
)

(cl:defclass GetRelevantPosition-request (<GetRelevantPosition-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetRelevantPosition-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetRelevantPosition-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name navigation-srv:<GetRelevantPosition-request> is deprecated: use navigation-srv:GetRelevantPosition-request instead.")))

(cl:ensure-generic-function 'relevantposition-val :lambda-list '(m))
(cl:defmethod relevantposition-val ((m <GetRelevantPosition-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation-srv:relevantposition-val is deprecated.  Use navigation-srv:relevantposition instead.")
  (relevantposition m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetRelevantPosition-request>) ostream)
  "Serializes a message object of type '<GetRelevantPosition-request>"
  (cl:let* ((signed (cl:slot-value msg 'relevantposition)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetRelevantPosition-request>) istream)
  "Deserializes a message object of type '<GetRelevantPosition-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'relevantposition) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetRelevantPosition-request>)))
  "Returns string type for a service object of type '<GetRelevantPosition-request>"
  "navigation/GetRelevantPositionRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetRelevantPosition-request)))
  "Returns string type for a service object of type 'GetRelevantPosition-request"
  "navigation/GetRelevantPositionRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetRelevantPosition-request>)))
  "Returns md5sum for a message object of type '<GetRelevantPosition-request>"
  "29c913f5cf74fb9a7ace0f16e99a4a40")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetRelevantPosition-request)))
  "Returns md5sum for a message object of type 'GetRelevantPosition-request"
  "29c913f5cf74fb9a7ace0f16e99a4a40")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetRelevantPosition-request>)))
  "Returns full string definition for message of type '<GetRelevantPosition-request>"
  (cl:format cl:nil "int32 relevantposition~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetRelevantPosition-request)))
  "Returns full string definition for message of type 'GetRelevantPosition-request"
  (cl:format cl:nil "int32 relevantposition~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetRelevantPosition-request>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetRelevantPosition-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetRelevantPosition-request
    (cl:cons ':relevantposition (relevantposition msg))
))
;//! \htmlinclude GetRelevantPosition-response.msg.html

(cl:defclass <GetRelevantPosition-response> (roslisp-msg-protocol:ros-message)
  ((status
    :reader status
    :initarg :status
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass GetRelevantPosition-response (<GetRelevantPosition-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetRelevantPosition-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetRelevantPosition-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name navigation-srv:<GetRelevantPosition-response> is deprecated: use navigation-srv:GetRelevantPosition-response instead.")))

(cl:ensure-generic-function 'status-val :lambda-list '(m))
(cl:defmethod status-val ((m <GetRelevantPosition-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation-srv:status-val is deprecated.  Use navigation-srv:status instead.")
  (status m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetRelevantPosition-response>) ostream)
  "Serializes a message object of type '<GetRelevantPosition-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'status) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetRelevantPosition-response>) istream)
  "Deserializes a message object of type '<GetRelevantPosition-response>"
    (cl:setf (cl:slot-value msg 'status) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetRelevantPosition-response>)))
  "Returns string type for a service object of type '<GetRelevantPosition-response>"
  "navigation/GetRelevantPositionResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetRelevantPosition-response)))
  "Returns string type for a service object of type 'GetRelevantPosition-response"
  "navigation/GetRelevantPositionResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetRelevantPosition-response>)))
  "Returns md5sum for a message object of type '<GetRelevantPosition-response>"
  "29c913f5cf74fb9a7ace0f16e99a4a40")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetRelevantPosition-response)))
  "Returns md5sum for a message object of type 'GetRelevantPosition-response"
  "29c913f5cf74fb9a7ace0f16e99a4a40")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetRelevantPosition-response>)))
  "Returns full string definition for message of type '<GetRelevantPosition-response>"
  (cl:format cl:nil "bool status~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetRelevantPosition-response)))
  "Returns full string definition for message of type 'GetRelevantPosition-response"
  (cl:format cl:nil "bool status~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetRelevantPosition-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetRelevantPosition-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetRelevantPosition-response
    (cl:cons ':status (status msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetRelevantPosition)))
  'GetRelevantPosition-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetRelevantPosition)))
  'GetRelevantPosition-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetRelevantPosition)))
  "Returns string type for a service object of type '<GetRelevantPosition>"
  "navigation/GetRelevantPosition")