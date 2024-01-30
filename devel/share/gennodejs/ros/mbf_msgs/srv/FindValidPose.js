// Auto-generated. Do not edit!

// (in-package mbf_msgs.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------


//-----------------------------------------------------------

class FindValidPoseRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pose = null;
      this.safety_dist = null;
      this.dist_tolerance = null;
      this.angle_tolerance = null;
      this.costmap = null;
      this.current_pose = null;
      this.use_padded_fp = null;
    }
    else {
      if (initObj.hasOwnProperty('pose')) {
        this.pose = initObj.pose
      }
      else {
        this.pose = new geometry_msgs.msg.PoseStamped();
      }
      if (initObj.hasOwnProperty('safety_dist')) {
        this.safety_dist = initObj.safety_dist
      }
      else {
        this.safety_dist = 0.0;
      }
      if (initObj.hasOwnProperty('dist_tolerance')) {
        this.dist_tolerance = initObj.dist_tolerance
      }
      else {
        this.dist_tolerance = 0.0;
      }
      if (initObj.hasOwnProperty('angle_tolerance')) {
        this.angle_tolerance = initObj.angle_tolerance
      }
      else {
        this.angle_tolerance = 0.0;
      }
      if (initObj.hasOwnProperty('costmap')) {
        this.costmap = initObj.costmap
      }
      else {
        this.costmap = 0;
      }
      if (initObj.hasOwnProperty('current_pose')) {
        this.current_pose = initObj.current_pose
      }
      else {
        this.current_pose = false;
      }
      if (initObj.hasOwnProperty('use_padded_fp')) {
        this.use_padded_fp = initObj.use_padded_fp
      }
      else {
        this.use_padded_fp = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type FindValidPoseRequest
    // Serialize message field [pose]
    bufferOffset = geometry_msgs.msg.PoseStamped.serialize(obj.pose, buffer, bufferOffset);
    // Serialize message field [safety_dist]
    bufferOffset = _serializer.float32(obj.safety_dist, buffer, bufferOffset);
    // Serialize message field [dist_tolerance]
    bufferOffset = _serializer.float32(obj.dist_tolerance, buffer, bufferOffset);
    // Serialize message field [angle_tolerance]
    bufferOffset = _serializer.float32(obj.angle_tolerance, buffer, bufferOffset);
    // Serialize message field [costmap]
    bufferOffset = _serializer.uint8(obj.costmap, buffer, bufferOffset);
    // Serialize message field [current_pose]
    bufferOffset = _serializer.bool(obj.current_pose, buffer, bufferOffset);
    // Serialize message field [use_padded_fp]
    bufferOffset = _serializer.bool(obj.use_padded_fp, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type FindValidPoseRequest
    let len;
    let data = new FindValidPoseRequest(null);
    // Deserialize message field [pose]
    data.pose = geometry_msgs.msg.PoseStamped.deserialize(buffer, bufferOffset);
    // Deserialize message field [safety_dist]
    data.safety_dist = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [dist_tolerance]
    data.dist_tolerance = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [angle_tolerance]
    data.angle_tolerance = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [costmap]
    data.costmap = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [current_pose]
    data.current_pose = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [use_padded_fp]
    data.use_padded_fp = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += geometry_msgs.msg.PoseStamped.getMessageSize(object.pose);
    return length + 15;
  }

  static datatype() {
    // Returns string type for a service object
    return 'mbf_msgs/FindValidPoseRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e0c36428252e9af85363d919831f88be';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # Find the closest free pose to the given one, within the given linear and angular tolerances.
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new FindValidPoseRequest(null);
    if (msg.pose !== undefined) {
      resolved.pose = geometry_msgs.msg.PoseStamped.Resolve(msg.pose)
    }
    else {
      resolved.pose = new geometry_msgs.msg.PoseStamped()
    }

    if (msg.safety_dist !== undefined) {
      resolved.safety_dist = msg.safety_dist;
    }
    else {
      resolved.safety_dist = 0.0
    }

    if (msg.dist_tolerance !== undefined) {
      resolved.dist_tolerance = msg.dist_tolerance;
    }
    else {
      resolved.dist_tolerance = 0.0
    }

    if (msg.angle_tolerance !== undefined) {
      resolved.angle_tolerance = msg.angle_tolerance;
    }
    else {
      resolved.angle_tolerance = 0.0
    }

    if (msg.costmap !== undefined) {
      resolved.costmap = msg.costmap;
    }
    else {
      resolved.costmap = 0
    }

    if (msg.current_pose !== undefined) {
      resolved.current_pose = msg.current_pose;
    }
    else {
      resolved.current_pose = false
    }

    if (msg.use_padded_fp !== undefined) {
      resolved.use_padded_fp = msg.use_padded_fp;
    }
    else {
      resolved.use_padded_fp = false
    }

    return resolved;
    }
};

// Constants for message
FindValidPoseRequest.Constants = {
  LOCAL_COSTMAP: 1,
  GLOBAL_COSTMAP: 2,
}

class FindValidPoseResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.state = null;
      this.cost = null;
      this.pose = null;
    }
    else {
      if (initObj.hasOwnProperty('state')) {
        this.state = initObj.state
      }
      else {
        this.state = 0;
      }
      if (initObj.hasOwnProperty('cost')) {
        this.cost = initObj.cost
      }
      else {
        this.cost = 0;
      }
      if (initObj.hasOwnProperty('pose')) {
        this.pose = initObj.pose
      }
      else {
        this.pose = new geometry_msgs.msg.PoseStamped();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type FindValidPoseResponse
    // Serialize message field [state]
    bufferOffset = _serializer.uint8(obj.state, buffer, bufferOffset);
    // Serialize message field [cost]
    bufferOffset = _serializer.uint32(obj.cost, buffer, bufferOffset);
    // Serialize message field [pose]
    bufferOffset = geometry_msgs.msg.PoseStamped.serialize(obj.pose, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type FindValidPoseResponse
    let len;
    let data = new FindValidPoseResponse(null);
    // Deserialize message field [state]
    data.state = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [cost]
    data.cost = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [pose]
    data.pose = geometry_msgs.msg.PoseStamped.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += geometry_msgs.msg.PoseStamped.getMessageSize(object.pose);
    return length + 5;
  }

  static datatype() {
    // Returns string type for a service object
    return 'mbf_msgs/FindValidPoseResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b6ece50286a64440b79a2c19db08c667';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new FindValidPoseResponse(null);
    if (msg.state !== undefined) {
      resolved.state = msg.state;
    }
    else {
      resolved.state = 0
    }

    if (msg.cost !== undefined) {
      resolved.cost = msg.cost;
    }
    else {
      resolved.cost = 0
    }

    if (msg.pose !== undefined) {
      resolved.pose = geometry_msgs.msg.PoseStamped.Resolve(msg.pose)
    }
    else {
      resolved.pose = new geometry_msgs.msg.PoseStamped()
    }

    return resolved;
    }
};

// Constants for message
FindValidPoseResponse.Constants = {
  FREE: 0,
  INSCRIBED: 1,
  LETHAL: 2,
  UNKNOWN: 3,
  OUTSIDE: 4,
}

module.exports = {
  Request: FindValidPoseRequest,
  Response: FindValidPoseResponse,
  md5sum() { return '3b058229757805d017574e238e310b27'; },
  datatype() { return 'mbf_msgs/FindValidPose'; }
};
