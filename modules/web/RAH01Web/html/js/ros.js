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
    divID : 'nav',
    width : elementWidth - 30,
    height : elementHeight
    });

    var nav = new NAV2D.OccupancyGridClientNav({
        ros: ros,
        rootObject: viewer.scene,
        viewer: viewer,
        serverName: '/move_base',
        continuous: true
    });

    var cmdVelListener = new ROSLIB.Topic({
        ros: ros,
        name: '/cmd_vel',
        messageType: 'geometry_msgs/Twist'
    });

    cmdVelListener.subscribe(function(message) {
        // Assuming message.linear.x and message.angular.z contain the speeds
        var linearSpeed = message.linear.x;
        var angularSpeed = message.angular.z;
    
        // Add data to the chart
        velocityChart.data.labels.push(new Date().toISOString()); // Add current time as label
        velocityChart.data.datasets[0].data.push(linearSpeed); // Add linear speed
        velocityChart.data.datasets[1].data.push(angularSpeed); // Add angular speed
    
        // Keep the number of data points manageable
        if(velocityChart.data.labels.length > 100) {
            velocityChart.data.labels.shift(); // Remove the oldest label
            velocityChart.data.datasets[0].data.shift(); // Remove the oldest linear speed data
            velocityChart.data.datasets[1].data.shift(); // Remove the oldest angular speed data
        }
    
        velocityChart.update();
    });

    var sampleJoystick = {
        zone: document.getElementById('joystick'),
        mode: 'static',
        position: {
            left: '80%',
            top: '90%'
        },
        size: 100,
        color: 'black'
    };

    var cmdVel = new ROSLIB.Topic({
        ros: ros, // Make sure this 'ros' object is correctly initialized and connected
        name: '/cmd_vel',
        messageType: 'geometry_msgs/Twist'
    });

    var joystick = nipplejs.create(sampleJoystick);

    joystick.on('move', function(evt, data) {
        // Constants for maximum speeds
        var maxLinearSpeed = 2.0;
        var maxAngularSpeed = 4.0;
    
        // Convert distance to a scale of 0 to 1
        var distanceNormalized = Math.min(data.distance / 100, 1); // Ensure the distance doesn't exceed 1
    
        // Angle in radians from the 'up' direction, adjusting for nipplejs's coordinate system
        var angleRadians = (data.angle.radian - Math.PI / 2) % (2 * Math.PI);
        if (angleRadians < 0) angleRadians += 2 * Math.PI; // Normalize angle to 0-2PI range
    
        // Calculate linear and angular velocities based on angle and distance
        // Linear velocity is highest when moving directly up or down (angleRadians close to 0 or PI)
        // Angular velocity is highest when moving directly left or right (angleRadians close to PI/2 or 3PI/2)
        var linear = Math.cos(angleRadians) * distanceNormalized * maxLinearSpeed;
        var angular = Math.sin(angleRadians) * distanceNormalized * maxAngularSpeed; // Negate to match expected rotation direction
    
        // Construct and send the Twist message
        var twist = new ROSLIB.Message({
            linear: {
                x: linear,
                y: 0.0,
                z: 0.0
            },
            angular: {
                x: 0.0,
                y: 0.0,
                z: angular
            }
        });
    
        cmdVel.publish(twist);
    });
    
    // Handle joystick release - stop the robot
    joystick.on('end', function() {
        var stopTwist = new ROSLIB.Message({
            linear: {
                x: 0,
                y: 0,
                z: 0
            },
            angular: {
                x: 0,
                y: 0,
                z: 0
            }
        });
    
        cmdVel.publish(stopTwist);
    });
}

window.addEventListener('DOMContentLoaded', (event) => {
    init();
});