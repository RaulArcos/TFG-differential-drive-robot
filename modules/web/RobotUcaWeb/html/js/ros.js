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
    continuous: true
    });

    gridClient.on('change', function() {
    viewer.scaleToDimensions(gridClient.currentGrid.width, gridClient.currentGrid.height);
    viewer.shift(gridClient.currentGrid.pose.position.x, gridClient.currentGrid.pose.position.y);
    });

    var robotMarker = new ROS2D.NavigationArrow({
        size : 0.25,
        strokeSize : 0.05,
        pulse: true,
        fillColor: createjs.Graphics.getRGB(255, 0, 0, 0.65)
    });

    gridClient.rootObject.addChild(robotMarker);

    var tfClient = new ROSLIB.TFClient({
        ros : ros,
        fixedFrame : 'map',
        angularThres : 0.01,
        transThres : 0.01
     });

    function tf_sub_func(tf) {
        console.log(tf);
        robotMarker.x = tf.translation.x;
        robotMarker.y = -tf.translation.y;
        robotMarker.rotation = new THREE.Euler().setFromQuaternion(new THREE.Quaternion(
              tf.rotation.x,
              tf.rotation.y,
              tf.rotation.z,
              tf.rotation.w
              )
          ).z * -180 / 3.14159;
      }

    tfClient.subscribe('base_footprint', tf_sub_func);
}

window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    init();
});