// Auto-generated. Do not edit!

// (in-package navigation.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class GetRelevantPositionRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.relevantposition = null;
    }
    else {
      if (initObj.hasOwnProperty('relevantposition')) {
        this.relevantposition = initObj.relevantposition
      }
      else {
        this.relevantposition = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetRelevantPositionRequest
    // Serialize message field [relevantposition]
    bufferOffset = _serializer.int32(obj.relevantposition, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetRelevantPositionRequest
    let len;
    let data = new GetRelevantPositionRequest(null);
    // Deserialize message field [relevantposition]
    data.relevantposition = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'navigation/GetRelevantPositionRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '06e83fb247ed357d986ea47c3a75b19a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 relevantposition
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetRelevantPositionRequest(null);
    if (msg.relevantposition !== undefined) {
      resolved.relevantposition = msg.relevantposition;
    }
    else {
      resolved.relevantposition = 0
    }

    return resolved;
    }
};

class GetRelevantPositionResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.status = null;
    }
    else {
      if (initObj.hasOwnProperty('status')) {
        this.status = initObj.status
      }
      else {
        this.status = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetRelevantPositionResponse
    // Serialize message field [status]
    bufferOffset = _serializer.bool(obj.status, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetRelevantPositionResponse
    let len;
    let data = new GetRelevantPositionResponse(null);
    // Deserialize message field [status]
    data.status = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'navigation/GetRelevantPositionResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '3a1255d4d998bd4d6585c64639b5ee9a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool status
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetRelevantPositionResponse(null);
    if (msg.status !== undefined) {
      resolved.status = msg.status;
    }
    else {
      resolved.status = false
    }

    return resolved;
    }
};

module.exports = {
  Request: GetRelevantPositionRequest,
  Response: GetRelevantPositionResponse,
  md5sum() { return '29c913f5cf74fb9a7ace0f16e99a4a40'; },
  datatype() { return 'navigation/GetRelevantPosition'; }
};
