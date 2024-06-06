// Generated by gencpp from file husky_gazebo_plugins/SetHuskyWheelSpeeds.msg
// DO NOT EDIT!


#ifndef HUSKY_GAZEBO_PLUGINS_MESSAGE_SETHUSKYWHEELSPEEDS_H
#define HUSKY_GAZEBO_PLUGINS_MESSAGE_SETHUSKYWHEELSPEEDS_H

#include <ros/service_traits.h>


#include <husky_gazebo_plugins/SetHuskyWheelSpeedsRequest.h>
#include <husky_gazebo_plugins/SetHuskyWheelSpeedsResponse.h>


namespace husky_gazebo_plugins
{

struct SetHuskyWheelSpeeds
{

typedef SetHuskyWheelSpeedsRequest Request;
typedef SetHuskyWheelSpeedsResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SetHuskyWheelSpeeds
} // namespace husky_gazebo_plugins


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeeds > {
  static const char* value()
  {
    return "ebe9a100c73aa02179b4e91ad134a89b";
  }

  static const char* value(const ::husky_gazebo_plugins::SetHuskyWheelSpeeds&) { return value(); }
};

template<>
struct DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeeds > {
  static const char* value()
  {
    return "husky_gazebo_plugins/SetHuskyWheelSpeeds";
  }

  static const char* value(const ::husky_gazebo_plugins::SetHuskyWheelSpeeds&) { return value(); }
};


// service_traits::MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeedsRequest> should match
// service_traits::MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >
template<>
struct MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeedsRequest>
{
  static const char* value()
  {
    return MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >::value();
  }
  static const char* value(const ::husky_gazebo_plugins::SetHuskyWheelSpeedsRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeedsRequest> should match
// service_traits::DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >
template<>
struct DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeedsRequest>
{
  static const char* value()
  {
    return DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >::value();
  }
  static const char* value(const ::husky_gazebo_plugins::SetHuskyWheelSpeedsRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeedsResponse> should match
// service_traits::MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >
template<>
struct MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeedsResponse>
{
  static const char* value()
  {
    return MD5Sum< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >::value();
  }
  static const char* value(const ::husky_gazebo_plugins::SetHuskyWheelSpeedsResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeedsResponse> should match
// service_traits::DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >
template<>
struct DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeedsResponse>
{
  static const char* value()
  {
    return DataType< ::husky_gazebo_plugins::SetHuskyWheelSpeeds >::value();
  }
  static const char* value(const ::husky_gazebo_plugins::SetHuskyWheelSpeedsResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // HUSKY_GAZEBO_PLUGINS_MESSAGE_SETHUSKYWHEELSPEEDS_H
