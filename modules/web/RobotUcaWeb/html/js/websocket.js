window.onload = function() {
    socket = new WebSocket("ws://localhost:5000/ws/video/");
    socket.addEventListener("open", (event) => {
        console.log("Connected to the videosocket.");
    });
    socket.addEventListener("message", (event) => {
        draw_img(event.data, "FrameCanvas");
    });

    socket.addEventListener("close", (event) => {
        if (event.wasClean) {
        console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
        } else {
        console.error("Connection abruptly closed");
        }
    });

    socket.addEventListener("error", (event) => {
        console.error("WebSocket error:", event);
    });
};

function draw_img(imdata, canvas_id, MAX_HEIGHT=720, MAX_WIDTH=1280){    
    var img = new Image();
    var canvasweb = document.getElementById(canvas_id);
    var rowWidth = canvasweb.parentNode.offsetWidth;
    var desiredWidth = rowWidth * 0.7;

    img.onload = function(){
        var originalWidth = img.width;
        var originalHeight = img.height;

        var desiredHeight = (originalHeight / originalWidth) * desiredWidth;

        canvasweb.width = desiredWidth;
        canvasweb.height = desiredHeight;

        var ctx = canvasweb.getContext("2d");
        ctx.clearRect(0, 0, canvasweb.width, canvasweb.height);
        ctx.drawImage(img, 0, 0, desiredWidth, desiredHeight);
    };

    img.src = "data:image/jpg;base64," + imdata;
}