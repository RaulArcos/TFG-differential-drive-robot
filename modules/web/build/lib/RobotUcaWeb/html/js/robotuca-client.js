function init() {
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

window.onload = function() {
  socket = new WebSocket("ws://localhost:5000/ws/video/");
  socket.addEventListener("open", (event) => {
    console.log("Connected to the videosocket.");
  });
  socket.addEventListener("message", (event) => {
    draw_img(event.data, "FrameCanvas");
  });

  // Connection closed
  socket.addEventListener("close", (event) => {
    if (event.wasClean) {
      console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
    } else {
      console.error("Connection abruptly closed");
    }
  });

  // Connection error
  socket.addEventListener("error", (event) => {
    console.error("WebSocket error:", event);
  });
};

function draw_img(imdata, canvas_id, MAX_HEIGHT=720, MAX_WIDTH=1280){    
  var img = new Image();
  var canvasweb = document.getElementById(canvas_id);
  var rowWidth = canvasweb.parentNode.offsetWidth; // Ancho de la celda padre
  var desiredWidth = rowWidth * 0.7; // El 70% del ancho de la celda

  img.onload = function(){
     
  // Obtiene las dimensiones originales de la imagen
     var originalWidth = img.width;
     var originalHeight = img.height;

     // Calcula la altura proporcional según el nuevo ancho deseado
     var desiredHeight = (originalHeight / originalWidth) * desiredWidth;

     // Establece las nuevas dimensiones al canvas
     canvasweb.width = desiredWidth;
     canvasweb.height = desiredHeight;

     // Dibuja la imagen en el canvas
     var ctx = canvasweb.getContext("2d");
     ctx.clearRect(0, 0, canvasweb.width, canvasweb.height);
     ctx.drawImage(img, 0, 0, desiredWidth, desiredHeight);
  };

  img.src = "data:image/jpg;base64," + imdata;
}

window.addEventListener('DOMContentLoaded', (event) => {
  console.log('DOM fully loaded and parsed');
  init();
});
