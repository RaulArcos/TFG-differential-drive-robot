import time
import threading
import cv2 as cv
import numpy as np
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst, GObject
from multiprocessing.pool import ThreadPool
from typing import List, Callable, Any

class gstVideoClient(object):
    _MAX_QUEUE_SIZE = 50
    def __init__(self):
        self._frame = None
        self._nframe = 0
        self._consume = True
        self._last_provided = -1
        self._use_queue = False
        self._queue = []
        self._keepAlive = 0
        self._pipeline = None
        self._timeout_id = None
        self._consumer_thread = threading.Thread(target=self._launch_pipeline)

    def init(self):
        try:
            self._consumer_thread.start()
        except:
            raise ConnectionError 

    def close(self) -> None:
        self._consume = False
        self._loop.quit()
        self._consumer_thread.join(5)
        
    def get_frame(self):
        return self._nframe, self._frame
        
    def _extract_frame(self, sink, _):
        self._keepAlive = time.time()
        sample = sink.emit("pull-sample")
        
        if not sample:
            return Gst.FlowReturn.OK
        
        buffer = sample.get_buffer()
        framecaps = sample.get_caps()
        s = framecaps.get_structure(0)
        width = s.get_int("width")[1]
        height = s.get_int("height")[1]

        result, map_info = buffer.map(Gst.MapFlags.READ)
        if not map_info:
            return Gst.FlowReturn.ERROR
        
        data = np.ndarray(shape=(height, width, 4), dtype=np.uint8, buffer=map_info.data)

        framec3 = cv.cvtColor(data, cv.COLOR_BGRA2BGR)
        framec3reduced = cv.resize(framec3, (640, 360), interpolation=cv.INTER_AREA)
  
        if framec3reduced.size > 0:
            ts = time.time()
            self._frame, self._nframe = framec3reduced, ts

        buffer.unmap(map_info)
        return Gst.FlowReturn.OK

    def _launch_pipeline(self):
        Gst.init(None)
        self._pipeline = Gst.Pipeline.new("pipeline")
        source = Gst.ElementFactory.make("shmsrc", "source")
        source.set_property("do-timestamp", True)
        source.set_property("is-live", True)

        caps = Gst.Caps.from_string("video/x-raw, width=1280, height=720, framerate=30/1, format=BGRx")

        source.set_property("socket-path", f"/tmp/rah01-socket-video")

        caps = Gst.Caps.from_string("video/x-raw, width=1280, height=720, framerate=30/1, format=BGRx")
        
        appsink = Gst.ElementFactory.make("appsink", "appsink")
        appsink.set_property("emit-signals", 1)
        appsink.set_property("drop", 0)
        appsink.set_property("max-buffers", 0)
        appsink.connect("new-sample", self._extract_frame, None)

        # self._pipeline.add(source)
        self._pipeline.add(source)
        self._pipeline.add(appsink)
        
        pad = source.link_filtered(appsink, caps)
        
        self._pipeline.set_state(Gst.State.PLAYING)
        self._timeout_id = GLib.timeout_add_seconds(0.5, self.check_alive)
        
        self._loop = GLib.MainLoop()
        self._loop.run()
        
    def check_alive(self):
        current_time = time.time()
        if current_time - self._keepAlive > 2:
            print("Current time", current_time, "keep alive", self._keepAlive)
            print("Timeout: ", current_time - self._keepAlive)
            print("Video lost, resetting pipeline")
            self._pipeline.set_state(Gst.State.NULL)
            self._pipeline.set_state(Gst.State.PLAYING)
            self._keepAlive = current_time
        
        return True