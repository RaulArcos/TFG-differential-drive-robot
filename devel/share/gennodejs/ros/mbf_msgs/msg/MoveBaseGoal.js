// Auto-generated. Do not edit!

// (in-package mbf_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class MoveBaseGoal {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.target_pose = null;
      this.controller = null;
      this.planner = null;
      this.recovery_behaviors = null;
    }
    else {
      if (initObj.hasOwnProperty('target_pose')) {
        this.target_pose = initObj.target_pose
      }
      else {
        this.target_pose = new geometry_msgs.msg.PoseStamped();
      }
      if (initObj.hasOwnProperty('controller')) {
        this.controller = initObj.controller
      }
      else {
        this.controller = '';
      }
      if (initObj.hasOwnProperty('planner')) {
        this.planner = initObj.planner
      }
      else {
        this.planner = '';
      }
      if (initObj.hasOwnProperty('recovery_behaviors')) {
        this.recovery_behaviors = initObj.recovery_behaviors
      }
      else {
        this.recovery_behaviors = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MoveBaseGoal
    // Serialize message field [target_pose]
    bufferOffset = geometry_msgs.msg.PoseStamped.serialize(obj.target_pose, buffer, bufferOffset);
    // Serialize message field [controller]
    bufferOffset = _serializer.string(obj.controller, buffer, bufferOffset);
    // Serialize message field [planner]
    bufferOffset = _serializer.string(obj.planner, buffer, bufferOffset);
    // Serialize message field [recovery_behaviors]
    bufferOffset = _arraySerializer.string(obj.recovery_behaviors, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MoveBaseGoal
    let len;
    let data = new MoveBaseGoal(null);
    // Deserialize message field [target_pose]
    data.target_pose = geometry_msgs.msg.PoseStamped.deserialize(buffer, bufferOffset);
    // Deserialize message field [controller]
    data.controller = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [planner]
    data.planner = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [recovery_behaviors]
    data.recovery_behaviors = _arrayDeserializer.string(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += geometry_msgs.msg.PoseStamped.getMessageSize(object.target_pose);
    length += _getByteLength(object.controller);
    length += _getByteLength(object.planner);
    object.recovery_behaviors.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'mbf_msgs/MoveBaseGoal';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '722601faf59588c53b718bb090b96808';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    # Extension of move_base_msgs/MoveBase action, with more detailed result
    # and feedback and the possibility to specify lists of applicable plugins
    
    geometry_msgs/PoseStamped target_pose
    
    # Controller to use; defaults to the first one specified on "controllers" parameter
    string controller
    
    # Planner to use; defaults to the first one specified on "planners" parameter
    string planner
    
    # Recovery behaviors to try on case of failure; defaults to the "recovery_behaviors" parameter value
    string[] recovery_behaviors
    
    
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
    const resolved = new MoveBaseGoal(null);
    if (msg.target_pose !== undefined) {
      resolved.target_pose = geometry_msgs.msg.PoseStamped.Resolve(msg.target_pose)
    }
    else {
      resolved.target_pose = new geometry_msgs.msg.PoseStamped()
    }

    if (msg.controller !== undefined) {
      resolved.controller = msg.controller;
    }
    else {
      resolved.controller = ''
    }

    if (msg.planner !== undefined) {
      resolved.planner = msg.planner;
    }
    else {
      resolved.planner = ''
    }

    if (msg.recovery_behaviors !== undefined) {
      resolved.recovery_behaviors = msg.recovery_behaviors;
    }
    else {
      resolved.recovery_behaviors = []
    }

    return resolved;
    }
};

module.exports = MoveBaseGoal;
