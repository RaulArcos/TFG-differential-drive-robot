function init() {
    var mapElement = document.getElementById('map');
    var mapColumn = document.getElementById('map-column');
    var elementStyles = window.getComputedStyle(mapColumn);
  
    var elementWidth = parseInt(elementStyles.width, 10);
    var elementHeight = parseInt(elementStyles.height, 10);
  
    var ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
    });

    var viewer = new ROS2D.Viewer({
    divID : 'map',
    width : elementWidth - 30,
    height : elementHeight
    });

    var gridClient = new ROS2D.OccupancyGridClient({
    ros : ros,
    rootObject : viewer.scene,
    viewer : viewer,
    continuous: true
    });

    gridClient.on('change', function() {
    viewer.scaleToDimensions(gridClient.currentGrid.width, gridClient.currentGrid.height);
    viewer.shift(gridClient.currentGrid.pose.position.x, gridClient.currentGrid.pose.position.y);
    });

    var robotMarker = new ROS2D.ArrowShape({
        size: 12,
        strokeSize: 1,
        fillColor: createjs.Graphics.getRGB(255, 128, 0, 0.66),
        pulse: true
    });
      
    // Function to update the robot's position on the map
    function updateRobotPosition(x, y, theta) {
    robotMarker.x = x;
    robotMarker.y = -y;
    robotMarker.rotation = theta;
    viewer.scene.addChild(robotMarker);
    }
    
    // Function to handle map click events
    function onMapClicked(event) {
    var local = viewer.scene.globalToLocal(event.stageX, event.stageY);
    
    // Convert to ROS coordinates
    var rosX = local.x;
    var rosY = -local.y;
    
    // Send these coordinates to the robot
    sendPositionCommand(rosX, rosY);
    }
    
    // Function to send position commands to the robot
    function sendPositionCommand(x, y) {
    var goal = new ROSLIB.Goal({
        actionClient : actionClient,
        goalMessage : {
        target_pose : {
            header : {
            frame_id : 'map'
            },
            pose : {
            position : { x: x, y: y, z: 0 },
            orientation : { x: 0, y: 0, z: 0, w: 1 }
            }
        }
        }
    });
    console.log('Sending goal')
    goal.send();
    }
    
    viewer.scene.addEventListener('stagemousedown', onMapClicked);

    var poseListener = new ROSLIB.Topic({
    ros : ros,
    name : '/odom',
    messageType : 'Odometry'
    });
    
    poseListener.subscribe(function(pose) {
    updateRobotPosition(odom.position.x, pose.position.y, pose.orientation.z);
    });
}

window.addEventListener('DOMContentLoaded', (event) => {
    init();
});