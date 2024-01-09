
export function init() {
  var mapElement = document.getElementById('map');
  var elementStyles = window.getComputedStyle(mapElement);

  var elementWidth = parseInt(elementStyles.width, 10);
  var elementHeight = parseInt(elementStyles.height, 10);

    var ros = new ROSLIB.Ros({
      url : 'ws://localhost:9090'
    });

    var viewer = new ROS2D.Viewer({
      divID : 'map',
      width : elementWidth,
      height : elementHeight
    });

    var gridClient = new ROS2D.OccupancyGridClient({
      ros : ros,
      rootObject : viewer.scene
    });

    gridClient.on('change', function() {
      viewer.scaleToDimensions(gridClient.currentGrid.width, gridClient.currentGrid.height);
      viewer.shift(gridClient.currentGrid.pose.position.x, gridClient.currentGrid.pose.position.y);
    });
}