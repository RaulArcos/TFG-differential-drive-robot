
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

function draw_img(imdata, canvas_id, MAX_HEIGHT=720, MAX_WIDTH=1280){    
  var img = new Image();
  var canvas = document.getElementById(canvas_id);
  var rowWidth = canvas.parentNode.offsetWidth; // Ancho de la celda padre
  var desiredWidth = rowWidth * 0.7; // El 70% del ancho de la celda

  img.onload = function(){
     
  // Obtiene las dimensiones originales de la imagen
     var originalWidth = img.width;
     var originalHeight = img.height;

     // Calcula la altura proporcional según el nuevo ancho deseado
     var desiredHeight = (originalHeight / originalWidth) * desiredWidth;

     // Establece las nuevas dimensiones al canvas
     canvas.width = desiredWidth;
     canvas.height = desiredHeight;

     // Dibuja la imagen en el canvas
     var ctx = canvas.getContext("2d");
     ctx.clearRect(0, 0, canvas.width, canvas.height);
     ctx.drawImage(img, 0, 0, desiredWidth, desiredHeight);
  };

  img.src = "data:image/jpg;base64," + imdata;
}
