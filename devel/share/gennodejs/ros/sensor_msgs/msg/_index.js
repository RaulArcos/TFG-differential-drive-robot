
"use strict";

let ChannelFloat32 = require('./ChannelFloat32.js');
let PointCloud = require('./PointCloud.js');
let LaserScan = require('./LaserScan.js');
let RelativeHumidity = require('./RelativeHumidity.js');
let MultiEchoLaserScan = require('./MultiEchoLaserScan.js');
let Image = require('./Image.js');
let JointState = require('./JointState.js');
let NavSatFix = require('./NavSatFix.js');
let JoyFeedback = require('./JoyFeedback.js');
let MultiDOFJointState = require('./MultiDOFJointState.js');
let BatteryState = require('./BatteryState.js');
let TimeReference = require('./TimeReference.js');
let CameraInfo = require('./CameraInfo.js');
let JoyFeedbackArray = require('./JoyFeedbackArray.js');
let NavSatStatus = require('./NavSatStatus.js');
let Imu = require('./Imu.js');
let Joy = require('./Joy.js');
let LaserEcho = require('./LaserEcho.js');
let Temperature = require('./Temperature.js');
let PointCloud2 = require('./PointCloud2.js');
let FluidPressure = require('./FluidPressure.js');
let CompressedImage = require('./CompressedImage.js');
let MagneticField = require('./MagneticField.js');
let Illuminance = require('./Illuminance.js');
let Range = require('./Range.js');
let PointField = require('./PointField.js');
let RegionOfInterest = require('./RegionOfInterest.js');

module.exports = {
  ChannelFloat32: ChannelFloat32,
  PointCloud: PointCloud,
  LaserScan: LaserScan,
  RelativeHumidity: RelativeHumidity,
  MultiEchoLaserScan: MultiEchoLaserScan,
  Image: Image,
  JointState: JointState,
  NavSatFix: NavSatFix,
  JoyFeedback: JoyFeedback,
  MultiDOFJointState: MultiDOFJointState,
  BatteryState: BatteryState,
  TimeReference: TimeReference,
  CameraInfo: CameraInfo,
  JoyFeedbackArray: JoyFeedbackArray,
  NavSatStatus: NavSatStatus,
  Imu: Imu,
  Joy: Joy,
  LaserEcho: LaserEcho,
  Temperature: Temperature,
  PointCloud2: PointCloud2,
  FluidPressure: FluidPressure,
  CompressedImage: CompressedImage,
  MagneticField: MagneticField,
  Illuminance: Illuminance,
  Range: Range,
  PointField: PointField,
  RegionOfInterest: RegionOfInterest,
};
