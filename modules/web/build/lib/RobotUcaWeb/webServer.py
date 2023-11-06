import asyncio
import base64
import cv2
import threading
from RobotUcaWeb.video_client import gstVideoClient
import websockets
import socketserver
import os
import functools
import http.server
import time

class WebServerManager():
    def __init__(self):
        self._lock = threading.Lock()
        self._videoClient = gstVideoClient()
        self._websocket_list = []
        self._http_port = 8080
        self._websocket_server = None
        self._http_ip = "localhost"
        self._network_mask = "255.255.255.0"
        self._network_gateway = "192.168.1.1"
        self._thread_stop = False
    
        self._videoClient.init()
        html_path = str(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")
        )
        os.chdir(html_path)

        socketserver.TCPServer.allow_reuse_address = True

        self._http_handler = functools.partial(http.server.SimpleHTTPRequestHandler)
        self._http_thread = threading.Thread(target=self._run_http_server)
        self._video_thread = threading.Thread(
            target=self._run_get_video_frames, daemon=True
        )
        self._websocket_server_thread = threading.Thread(
            target=self._run_websocket_server, daemon=True
        )

        self._http_thread.start()
        self._video_thread.start()
        self._websocket_server_thread.start()
        

    def _run_websocket_server(self):
        async def router(websocket, path):
            if path == "/ws/video/":
                print("hey")
                await self.webserver_image(websocket, path)

        async def websockets_main():
            async with websockets.serve(router, None, 8080, reuse_address=True, reuse_port=True) as self._websocket_server:
                await asyncio.Future()
        asyncio.run(websockets_main())

    def _run_get_video_frames(self):
            _, frame = self._videoClient.get_frame()
            if frame is not None:
                _, im_arr = cv2.imencode(".jpg", frame)
                im_b64 = base64.b64encode(im_arr).decode("utf-8")
                with self.lock:                
                    async def send_frame_async(websocket_list):
                        tasks = []
                        for websocket in set(websocket_list):
                            tasks.append(websocket.send(im_b64))
                        await asyncio.gather(*tasks)

                    async def send(websocket_list):
                        await send_frame_async(websocket_list)

                    async def send_main():
                        try:
                            await send(self._websocket_list)
                        except Exception as e:
                            print(e)

                    asyncio.run(send_main())
    
    async def webserver_image(self, websocket: websockets.WebSocketServerProtocol, path):
        self._websocket_list.append(websocket)
    
    def _run_http_server(self):
        httpd = socketserver.TCPServer(("", self._http_port), self._http_handler)
        httpd.serve_forever()
        self._trigger_reload = True
    
    async def webserver_routine(self, websocket: websockets.WebSocketServerProtocol, path):
        while True:
            if self._trigger_reload:
                await websocket.send("RELOAD")
                self._trigger_reload = False
            await asyncio.sleep(0.03)

if __name__ == "__main__":
    web = WebServerManager()