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
}

window.addEventListener('DOMContentLoaded', (event) => {
    init();
});