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

    // setup the actionlib client
    var actionClient = new ROSLIB.ActionClient({
        ros: ros,
        actionName: actionName,
        serverName: serverName
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
     * Send a goal to the navigation stack with the given pose.
     *
     * @param pose - the goal pose
     */
    function sendGoal(pose) {
        var targetPath;


        var goal = new ROSLIB.Goal({
            actionClient: actionClient,
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
            pulse: true
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

    window.pathed = function() {

        pathView = new ROS2D.PathShape({
            ros: ros,
            strokeSize: 0.1,
            strokeColor: "green",
        });

        that.rootObject.addChild(pathView);

        pathTopic = new ROSLIB.Topic({
            ros: ros,
            name: '/move_base/NavfnROS/plan',
            messageType: 'nav_msgs/Path'
        });

        pathTopic.subscribe(function(message) {
            pathView.setPath(message);
        });

    }

    window.upathed = function() {
        that.rootObject.removeChild(pathView);
        if (pathTopic) {
            pathTopic.unsubscribe();
        }
        pathView = null;
        pathTopic = null;
    }
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