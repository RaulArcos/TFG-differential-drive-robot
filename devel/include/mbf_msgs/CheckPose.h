// Generated by gencpp from file mbf_msgs/CheckPose.msg
// DO NOT EDIT!


#ifndef MBF_MSGS_MESSAGE_CHECKPOSE_H
#define MBF_MSGS_MESSAGE_CHECKPOSE_H

#include <ros/service_traits.h>


#include <mbf_msgs/CheckPoseRequest.h>
#include <mbf_msgs/CheckPoseResponse.h>


namespace mbf_msgs
{

struct CheckPose
{

typedef CheckPoseRequest Request;
typedef CheckPoseResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct CheckPose
} // namespace mbf_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::mbf_msgs::CheckPose > {
  static const char* value()
  {
    return "49306eb70b373b82a480a121a2f03a15";
  }

  static const char* value(const ::mbf_msgs::CheckPose&) { return value(); }
};

template<>
struct DataType< ::mbf_msgs::CheckPose > {
  static const char* value()
  {
    return "mbf_msgs/CheckPose";
  }

  static const char* value(const ::mbf_msgs::CheckPose&) { return value(); }
};


// service_traits::MD5Sum< ::mbf_msgs::CheckPoseRequest> should match
// service_traits::MD5Sum< ::mbf_msgs::CheckPose >
template<>
struct MD5Sum< ::mbf_msgs::CheckPoseRequest>
{
  static const char* value()
  {
    return MD5Sum< ::mbf_msgs::CheckPose >::value();
  }
  static const char* value(const ::mbf_msgs::CheckPoseRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::mbf_msgs::CheckPoseRequest> should match
// service_traits::DataType< ::mbf_msgs::CheckPose >
template<>
struct DataType< ::mbf_msgs::CheckPoseRequest>
{
  static const char* value()
  {
    return DataType< ::mbf_msgs::CheckPose >::value();
  }
  static const char* value(const ::mbf_msgs::CheckPoseRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::mbf_msgs::CheckPoseResponse> should match
// service_traits::MD5Sum< ::mbf_msgs::CheckPose >
template<>
struct MD5Sum< ::mbf_msgs::CheckPoseResponse>
{
  static const char* value()
  {
    return MD5Sum< ::mbf_msgs::CheckPose >::value();
  }
  static const char* value(const ::mbf_msgs::CheckPoseResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::mbf_msgs::CheckPoseResponse> should match
// service_traits::DataType< ::mbf_msgs::CheckPose >
template<>
struct DataType< ::mbf_msgs::CheckPoseResponse>
{
  static const char* value()
  {
    return DataType< ::mbf_msgs::CheckPose >::value();
  }
  static const char* value(const ::mbf_msgs::CheckPoseResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // MBF_MSGS_MESSAGE_CHECKPOSE_H
