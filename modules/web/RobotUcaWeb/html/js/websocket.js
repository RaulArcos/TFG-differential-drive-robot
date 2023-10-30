function startConnectionSocketImage() {
    console.log("WebSocket 'image' onload");
    var ws_address_image = "ws://" + variables.http_ip.value + ":5000/ws/video/";
    console.log(ws_address_image);
    variables.wsocket_image.assign(new WebSocket(ws_address_image));
    console.log("WebSocket 'image' created");
 
    variables.wsocket_image.value.onopen = function () { onOpenImage(); };
    variables.wsocket_image.value.onmessage = function (evt) { onMessageImage(evt); };
    variables.wsocket_image.value.onclose = function () { onCloseImage(); };
    variables.wsocket_image.value.onerror = function () { onErrorImage(); };
 }

function onMessageImage(evt) {
    var str_data = String(evt.data);
 
    if (str_data.startsWith(variables.im_header.value) && variables.cfg.value.video_web) {
       displays.draw_img(evt.data, "FrameCanvas2");
       displays.draw_img(evt.data, "FrameCanvas");
    }
    else if (!variables.cfg.value.video_web) {
       displays.clearCanvas(document.getElementById("FrameCanvas2"));
       displays.clearCanvas(document.getElementById("FrameCanvas"));
    }
}

function robotuca_initialization() {
   console.log(window.location.href);
   http_ip.assign(window.location.href);
   http_ip.assign(http_ip.value.replaceAll('/', ''));
   http_ip.assign(http_ip.value.split(":")[1]);
   console.log(http_ip.value);

   startConnectionSocketImage();
   wsocket_in.value.onload = changeTab("info-area-general");
}

window.addEventListener("load", robotuca_initialization, false);
window.onload = function () { displays.charts(); };