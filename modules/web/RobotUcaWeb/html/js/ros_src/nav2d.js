var NAV2D = NAV2D || {
    REVISION: '0.3.0'
};

var count =null;
var robotvisible=false;

NAV2D.ImageMapClientNav = function(options) {
    var that = this;
    options = options || {};
    this.ros = options.ros;
    var topic = options.topic || '/map_metadata';
    var image = options.image;
    this.serverName = options.serverName || '/move_base';
    this.actionName = options.actionName || 'move_base_msgs/MoveBaseAction';
    this.rootObject = options.rootObject || new createjs.Container();
    this.viewer = options.viewer;
    this.withOrientation = options.withOrientation || true;
    this.navigator = null;

    // setup a client to get the map
    var client = new ROS2D.ImageMapClient({
        ros: this.ros,
        rootObject: this.rootObject,
        topic: topic,
        image: image
    });
    client.on('change', function() {

        that.navigator = new NAV2D.Navigator({
            ros: that.ros,
            serverName: that.serverName,
            actionName: that.actionName,
            rootObject: that.rootObject,
            withOrientation: that.withOrientation
        });


        // scale the viewer to fit the map

        that.viewer.scaleToDimensions(client.currentImage.width, client.currentImage.height);

        that.viewer.shift(client.currentImage.pose.position.x, client.currentImage.pose.position.y);

    });

    this.removeImg = client.removeImg;

    this.addImg = client.addImg;
   
};

NAV2D.Navigator = function(options) {
    var that = this;
    options = options || {};
    var ros = options.ros;
    var serverName = options.serverName || '/move_base';
    var actionName = options.actionName || 'move_base_msgs/MoveBaseAction';
    var withOrientation = options.withOrientation || true;
    this.rootObject = options.rootObject || new createjs.Container();

    var homing = false;
    var navigation = false;

    document.getElementById('set-location').addEventListener('click', function() {
        // Toggle homing mode
        homing = !homing;
        // Ensure navigation is disabled when homing is enabled
        if (homing) {
            navigation = false;
            console.log('Homing mode enabled');
        } else {
            console.log('Homing mode disabled');
        }
    });

    document.getElementById('set-goal').addEventListener('click', function() {
        // Toggle navigation mode
        navigation = !navigation;
        // Ensure homing is disabled when navigation is enabled
        if (navigation) {
            homing = false;
            console.log('Navigation mode enabled');
        } else {
            console.log('Navigation mode disabled');
        }
    });

    // setup the actionlib client
    var actionClient = new ROSLIB.ActionClient({
        ros: ros,
        actionName: actionName,
        serverName: serverName
    });

    var actionClientGoal = new ROSLIB.ActionClient({
        ros: ros,
        actionName: "move_base_msgs/MoveBaseAction",
        serverName: "/move_base_simple"
    });

    function homefunc(pose) {
        var robot = new ROSLIB.Topic({
            ros: ros,
            name: '/initialpose',
            messageType: 'geometry_msgs/PoseWithCovarianceStamped'
        });

        var posee = new ROSLIB.Message({ header: { frame_id: "map" }, pose: { pose: { position: { x: pose.position.x, y: pose.position.y, z: 0.0 }, orientation: { z: pose.orientation.z, w: pose.orientation.w } }, covariance: [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942] } });
        robot.publish(posee);
        homing = false;
        navigation = false;
    }

    /**
     * @author Raul Arcos Herrera 
     */

    function subscribeToMoveBaseStatus() {
        var statusSubscriber = new ROSLIB.Topic({
            ros: ros,
            name: '/move_base/status',
            messageType: 'actionlib_msgs/GoalStatusArray'
        });
    
        var cmdVelSubscriber = new ROSLIB.Topic({
            ros: ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/Twist'
        });
    
        // Variable to track if there is any movement
        var isMoving = false;
    
        // Subscribe to cmd_vel to update isMoving
        cmdVelSubscriber.subscribe(function(message) {
            // Assuming linear or angular velocity indicates movement
            // You may need to adjust this condition based on your specific robot
            isMoving = message.linear.x !== 0 || message.angular.z !== 0;
        });
    
        statusSubscriber.subscribe(function(message) {
            var statusBox = document.getElementById('status-box');
            if (!message.status_list.length) {
                statusBox.innerHTML = 'waiting...';
                statusBox.style.color = 'red';
            } else {
                var latestStatus = message.status_list[message.status_list.length - 1].status;
                switch (latestStatus) {
                    case 0: // PENDING
                    case 1: // ACTIVE
                        if (isMoving) {
                            statusBox.innerHTML = 'moving';
                            statusBox.style.backgroundColor = 'lightgreen';
                        } else {
                            // Status is ACTIVE but not moving yet, so "thinking"
                            statusBox.innerHTML = 'thinking';
                            statusBox.style.backgroundColor = 'lightblue';
                        }
                        break;
                    case 3: // SUCCEEDED
                        statusBox.innerHTML = 'goal reached!';
                        statusBox.style.backgroundColor = 'purple';
                        break;
                    default:
                        // This covers other statuses
                        statusBox.innerHTML = 'moving';
                        statusBox.style.backgroundColor = 'green';
                }
            }
        });
    }

    function subscribeAndPaintLaserScans() {
        var scanSubscriber = new ROSLIB.Topic({
            ros: ros,
            name: '/scan',
            messageType: 'sensor_msgs/LaserScan'
        });
    
        var scanPoints = new createjs.Shape();
        that.rootObject.addChild(scanPoints);
    
        scanSubscriber.subscribe(function(message) {
            scanPoints.graphics.clear();
    
            var adjustedRobotRotationRadians = (robotMarker.rotation+180) * (Math.PI / 180);
    
            var angle = message.angle_min;
            for (var i = 0; i < message.ranges.length; i++) {
                var range = message.ranges[i];
                if (range >= message.range_min && range <= message.range_max) {
          
                    var correctedAngle = angle - adjustedRobotRotationRadians;
                    var laserX = range * Math.cos(correctedAngle);
                    var laserY = range * Math.sin(correctedAngle)*-1;

                    var transformedX = laserX + robotMarker.x;
                    var transformedY = laserY + robotMarker.y; 
    
                    scanPoints.graphics.beginFill("#FF0000").drawCircle(transformedX, transformedY, 0.1);
                }
                angle += message.angle_increment;
            }
    
            stage.update();
        });
    }

    var goalTopic = new ROSLIB.Topic({
        ros: ros,
        name: '/move_base_simple/goal',
        messageType: 'geometry_msgs/PoseStamped'
    });

    var currentGoalMarker = null;

    function subscribeToGoalAndDisplayMarker() {
        // Goal position subscription
        var goalSubscriber = new ROSLIB.Topic({
            ros: ros,
            name: 'move_base_simple/goal',
            messageType: 'geometry_msgs/PoseStamped'
        });
    
        goalSubscriber.subscribe(function(message) {
            // Clear the previous goal marker, if any
            if (currentGoalMarker) {
                that.rootObject.removeChild(currentGoalMarker);
                currentGoalMarker = null;
            }
    
            // Extract pose from the message
            var pose = message.pose;
    
            // Create and display the new goal marker
            currentGoalMarker = createGoalMarker(pose);
            that.rootObject.addChild(currentGoalMarker);
        });
    
        // Goal status subscription
        var statusSubscriber = new ROSLIB.Topic({
            ros: ros,
            name: '/move_base/status',
            messageType: 'actionlib_msgs/GoalStatusArray'
        });
    
        statusSubscriber.subscribe(function(statusMessage) {
            // Check the status array for any goal that has reached status
            var goalReached = statusMessage.status_list.some(function(status) {
                return status.status === 3; // Status 3 indicates success
            });
    
            if (goalReached && currentGoalMarker) {
                // Optionally, change the goal marker's appearance or remove it
                // For now, let's remove it
                that.rootObject.removeChild(currentGoalMarker);
                currentGoalMarker = null;
            }
        });
    }
    
    function createGoalMarker(pose) {
        // This function encapsulates the creation of the goal marker
        var goalMarker = new ROS2D.NavigationArrow({
            size: 15,
            strokeSize: 1,
            fillColor: createjs.Graphics.getRGB(255, 64, 128, 0.66),
            pulse: false
        });
    
        goalMarker.x = pose.position.x;
        goalMarker.y = -pose.position.y;
        goalMarker.rotation = stage.rosQuaternionToGlobalTheta(pose.orientation);
        goalMarker.scaleX = 1.0 / stage.scaleX;
        goalMarker.scaleY = 1.0 / stage.scaleY;
    
        return goalMarker;
    }

    function sendSimpleGoal(pose) {
        // Create the goal message
        var goalMsg = new ROSLIB.Message({
            header: {
                frame_id: 'map' // Make sure this is the correct frame for your use case
            },
            pose: {
                position: {
                    x: pose.position.x,
                    y: pose.position.y,
                    z: pose.position.z
                },
                orientation: {
                    x: pose.orientation.x,
                    y: pose.orientation.y,
                    z: pose.orientation.z,
                    w: pose.orientation.w
                }
            }
        });
    
        // Publish the message
        goalTopic.publish(goalMsg);

        // var goalMarker = new ROS2D.NavigationArrow({
        //     size: 15,
        //     strokeSize: 1,
        //     fillColor: createjs.Graphics.getRGB(255, 64, 128, 0.66),
        //     pulse: false
        // });

        // goalMarker.x = pose.position.x;
        // goalMarker.y = -pose.position.y;
        // goalMarker.rotation = stage.rosQuaternionToGlobalTheta(pose.orientation);
        // goalMarker.scaleX = 1.0 / stage.scaleX;
        // goalMarker.scaleY = 1.0 / stage.scaleY;
        // that.rootObject.addChild(goalMarker);

        //TODO: LISTENERS

        // goal.on('result', function() {
        //     that.rootObject.removeChild(goalMarker);
        //     navigation = false;

        // });
    }

    /**
     * Send a goal to the navigation stack with the given pose.
     *
     * @param pose - the goal pose
     */
    function sendGoal(pose) {
        var targetPath;

        var goal = new ROSLIB.Goal({
            actionClient: actionClientGoal,
            goalMessage: {
                target_pose: {
                    header: {
                        frame_id: '/map'
                    },
                    pose: pose
                }
            }
        });

        goal.send();



        var goalMarker = new ROS2D.NavigationArrow({
            size: 15,
            strokeSize: 1,
            fillColor: createjs.Graphics.getRGB(255, 64, 128, 0.66),
            pulse: false
        });

        goalMarker.x = pose.position.x;
        goalMarker.y = -pose.position.y;
        goalMarker.rotation = stage.rosQuaternionToGlobalTheta(pose.orientation);
        goalMarker.scaleX = 1.0 / stage.scaleX;
        goalMarker.scaleY = 1.0 / stage.scaleY;
        that.rootObject.addChild(goalMarker);

        goal.on('result', function() {
            that.rootObject.removeChild(goalMarker);
            navigation = false;

        });
    }

    // get a handle to the stage

    var stage;

    if (that.rootObject instanceof createjs.Stage) {
        stage = that.rootObject;
    } else {
        stage = that.rootObject.getStage();
    }

    // marker for the robot
    var robotMarker = new ROS2D.NavigationArrow({
    size : 25,
    strokeSize : 1,
    fillColor : createjs.Graphics.getRGB(255, 128, 0, 0.66),
    pulse : true
  });

    // wait for a pose to come in first
    robotMarker.visible = false;


    count=count+1
    if (count == 1 || robotvisible == true){
        that.rootObject.addChild(robotMarker);
        robotvisible=false;
    }
  

    var initScaleSet = false;

    // setup a listener for the robot pose
    var poseListener = new ROSLIB.Topic({
        ros: ros,
        name: '/amcl_pose',
        messageType: 'geometry_msgs/PoseWithCovarianceStamped',
        throttle_rate: 1
    });

    poseListener.subscribe(function(pose) {
        // update the robots position on the map
        robotMarker.x = pose.pose.pose.position.x;
        robotMarker.y = -pose.pose.pose.position.y;

        if (!initScaleSet) {
        robotMarker.scaleX = 1.0 / stage.scaleX;
        robotMarker.scaleY = 1.0 / stage.scaleY;
        initScaleSet = true;
        }

        // change the angle
        robotMarker.rotation = stage.rosQuaternionToGlobalTheta(pose.pose.pose.orientation);
        robotMarker.visible = true;
    });

    var pathView = null,
    pathTopic = null;

    var pathShape; // Define globally to access in different functions

    function subscribeToNavPlanAndPaintPath() {
        var planSubscriber = new ROSLIB.Topic({
            ros: ros,
            name: '/move_base/NavfnROS/plan',
            messageType: 'nav_msgs/Path'
        });
    
        planSubscriber.subscribe(function(message) {
            // Check if there's an existing path and remove it
            if (pathShape) {
                that.rootObject.removeChild(pathShape);
                pathShape = null;
            }
    
            // Ensure message.poses is defined and contains at least one pose
            if (message.poses && message.poses.length > 0) {
                // Proceed to create and draw the path
                pathShape = new ROS2D.PathShape({
                    strokeSize: 1, // Thickness of the path
                    strokeColor: createjs.Graphics.getRGB(0, 255, 0), // Color of the path
                    path: message.poses, // The series of poses representing the path
                    scaleX: 1.0, // Assuming scaleX is 1.0, adjust as necessary
                    scaleY: 1.0 // Assuming scaleY is 1.0, adjust as necessary
                });
    
                // Add the path shape to the root object for rendering
                that.rootObject.addChild(pathShape);
            } else {
                console.log('No poses received in the navigation plan.');
            }
        });
    }    

    var position = null;
    var positionVec3 = null;
    var thetaRadians = 0;
    var thetaDegrees = 0;
    var orientationMarker = null;
    var mouseDown = false;
    var xDelta = 0;
    var yDelta = 0;
    var panflag = true;

    var pannavfunction = function(event, mouseState) {
        // label:
        if (navigation == true || homing == true) {
            // var mouseEventHandler = function(event, mouseState) {

            if (mouseState === 'down') {
                // get position when mouse button is pressed down
                position = stage.globalToRos(event.stageX, event.stageY);
                positionVec3 = new ROSLIB.Vector3(position);
                mouseDown = true;
            } else if (mouseState === 'move') {
                // remove obsolete orientation marker
                that.rootObject.removeChild(orientationMarker);

                if (mouseDown === true) {

                    // if mouse button is held down:
                    // - get current mouse position
                    // - calulate direction between stored <position> and current position
                    // - place orientation marker
                    var currentPos = stage.globalToRos(event.stageX, event.stageY);
                    var currentPosVec3 = new ROSLIB.Vector3(currentPos);

                    orientationMarker = new ROS2D.NavigationArrow({
                        size: 25,
                        strokeSize: 1,
                        fillColor: createjs.Graphics.getRGB(0, 255, 0, 0.66),
                        pulse: false
                    });

                    xDelta = currentPosVec3.x - positionVec3.x;
                    yDelta = currentPosVec3.y - positionVec3.y;

                    thetaRadians = Math.atan2(xDelta, yDelta);

                    thetaDegrees = thetaRadians * (180.0 / Math.PI);

                    if (thetaDegrees >= 0 && thetaDegrees <= 180) {
                        thetaDegrees += 270;
                    } else {
                        thetaDegrees -= 90;
                    }

                    orientationMarker.x = positionVec3.x;
                    orientationMarker.y = -positionVec3.y;
                    orientationMarker.rotation = thetaDegrees;
                    orientationMarker.scaleX = 1.0 / stage.scaleX;
                    orientationMarker.scaleY = 1.0 / stage.scaleY;
                        that.rootObject.addChild(orientationMarker);
                    
                
            }} else if (mouseDown) { // mouseState === 'up'
                // if mouse button is released
                // - get current mouse position (goalPos)
                // - calulate direction between stored <position> and goal position
                // - set pose with orientation
                // - send goal
                mouseDown = false;


                var goalPos = stage.globalToRos(event.stageX, event.stageY);

                var goalPosVec3 = new ROSLIB.Vector3(goalPos);

                xDelta = goalPosVec3.x - positionVec3.x;
                yDelta = goalPosVec3.y - positionVec3.y;

                thetaRadians = Math.atan2(xDelta, yDelta);

                if (thetaRadians >= 0 && thetaRadians <= Math.PI) {
                    thetaRadians += (3 * Math.PI / 2);
                } else {
                    thetaRadians -= (Math.PI / 2);
                }

                var qz = Math.sin(-thetaRadians / 2.0);
                var qw = Math.cos(-thetaRadians / 2.0);

                var orientation = new ROSLIB.Quaternion({
                    x: 0,
                    y: 0,
                    z: qz,
                    w: qw
                });

                var pose = new ROSLIB.Pose({
                    position: positionVec3,
                    orientation: orientation
                });
                // send the goal
                if (navigation == true) {
                    console.log(pose)
                    sendSimpleGoal(pose);
                }
                if (homing == true) {
                    homefunc(pose);
                }

                navigation = false;

            }
        }
            if (!homing && !navigation) {
                if (mouseState === 'down' && typeof pane === "function") {
                    pane(event.stageX, event.stageY);
                    panflag = true;
                } else if (mouseState === 'up') {
                    // console.log("hi up here");
                    panflag = false;
                } else if (mouseState === 'move' && typeof pane === "function") {
                    mouseDown = false;
                    that.rootObject.removeChild(orientationMarker);
                    if (panflag) {
                        paned(event.stageX, event.stageY);
                    }
                }
            }
    };

    this.rootObject.addEventListener('stagemousedown', function(event) {
        pannavfunction(event, 'down');
        that.rootObject.addEventListener('stagemousemove', function(event) {
            pannavfunction(event, 'move');

        });

    });

    this.rootObject.addEventListener('stagemouseup', function(event) {
        pannavfunction(event, 'up');
    });

    subscribeToGoalAndDisplayMarker();
    subscribeAndPaintLaserScans();
    // subscribeToNavPlanAndPaintPath();
    subscribeToMoveBaseStatus();
};

NAV2D.OccupancyGridClientNav = function(options) {
    var that = this;
    options = options || {};
    this.ros = options.ros;
    var topic = options.topic || '/map';
    var continuous = options.continuous;
    this.serverName = options.serverName || '/move_base';
    this.actionName = options.actionName || 'move_base_msgs/MoveBaseAction';
    this.rootObject = options.rootObject || new createjs.Container();
    this.viewer = options.viewer;
    this.withOrientation = options.withOrientation || true;
    this.navigator = null;

    // setup a client to get the map
    var client = new ROS2D.OccupancyGridClient({
        ros: this.ros,
        rootObject: this.rootObject,
        continuous: continuous,
        topic: topic
    });
    client.on('change', function() {

        that.navigator = new NAV2D.Navigator({
            ros: that.ros,
            serverName: that.serverName,
            actionName: that.actionName,
            rootObject: that.rootObject,
            withOrientation: that.withOrientation
        });

        // scale the viewer to fit the map
        that.viewer.scaleToDimensions(client.currentGrid.width, client.currentGrid.height);
        that.viewer.shift(client.currentGrid.pose.position.x, client.currentGrid.pose.position.y);
    });

};