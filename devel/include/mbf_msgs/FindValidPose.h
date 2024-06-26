// Generated by gencpp from file mbf_msgs/FindValidPose.msg
// DO NOT EDIT!


#ifndef MBF_MSGS_MESSAGE_FINDVALIDPOSE_H
#define MBF_MSGS_MESSAGE_FINDVALIDPOSE_H

#include <ros/service_traits.h>


#include <mbf_msgs/FindValidPoseRequest.h>
#include <mbf_msgs/FindValidPoseResponse.h>


namespace mbf_msgs
{

struct FindValidPose
{

typedef FindValidPoseRequest Request;
typedef FindValidPoseResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct FindValidPose
} // namespace mbf_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::mbf_msgs::FindValidPose > {
  static const char* value()
  {
    return "3b058229757805d017574e238e310b27";
  }

  static const char* value(const ::mbf_msgs::FindValidPose&) { return value(); }
};

template<>
struct DataType< ::mbf_msgs::FindValidPose > {
  static const char* value()
  {
    return "mbf_msgs/FindValidPose";
  }

  static const char* value(const ::mbf_msgs::FindValidPose&) { return value(); }
};


// service_traits::MD5Sum< ::mbf_msgs::FindValidPoseRequest> should match
// service_traits::MD5Sum< ::mbf_msgs::FindValidPose >
template<>
struct MD5Sum< ::mbf_msgs::FindValidPoseRequest>
{
  static const char* value()
  {
    return MD5Sum< ::mbf_msgs::FindValidPose >::value();
  }
  static const char* value(const ::mbf_msgs::FindValidPoseRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::mbf_msgs::FindValidPoseRequest> should match
// service_traits::DataType< ::mbf_msgs::FindValidPose >
template<>
struct DataType< ::mbf_msgs::FindValidPoseRequest>
{
  static const char* value()
  {
    return DataType< ::mbf_msgs::FindValidPose >::value();
  }
  static const char* value(const ::mbf_msgs::FindValidPoseRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::mbf_msgs::FindValidPoseResponse> should match
// service_traits::MD5Sum< ::mbf_msgs::FindValidPose >
template<>
struct MD5Sum< ::mbf_msgs::FindValidPoseResponse>
{
  static const char* value()
  {
    return MD5Sum< ::mbf_msgs::FindValidPose >::value();
  }
  static const char* value(const ::mbf_msgs::FindValidPoseResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::mbf_msgs::FindValidPoseResponse> should match
// service_traits::DataType< ::mbf_msgs::FindValidPose >
template<>
struct DataType< ::mbf_msgs::FindValidPoseResponse>
{
  static const char* value()
  {
    return DataType< ::mbf_msgs::FindValidPose >::value();
  }
  static const char* value(const ::mbf_msgs::FindValidPoseResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // MBF_MSGS_MESSAGE_FINDVALIDPOSE_H
