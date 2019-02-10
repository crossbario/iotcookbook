import base64
import threading
import uuid

import cv2
from autobahn.twisted import wamp
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor, threads


# Inspired by http://blog.blitzblit.com/2017/12/24/asynchronous-video-capture-in-python-with-opencv/
class AsyncFrameReader:
    def __init__(self, src=0, width=1280, height=720):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed = False
        self.frame = None
        self.started = False
        self.read_lock = threading.Lock()
        self.listeners = []

    def add_on_frame_listener(self, func):
        self.listeners.append(func)

    def start(self):
        if not self.started:
            self.started = True
            threads.deferToThread(self.update)

    def update(self):
        while self.started and reactor.running:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame
            for listener in self.listeners:
                threads.deferToThread(listener)

    def read(self):
        with self.read_lock:
            return self.grabbed, self.frame.copy()

    def stop(self):
        self.started = False
        self.cap.stop()


class ClientSession(wamp.ApplicationSession):
    def capture_and_send_frames(self):
        def on_frame():
            ret, frame = reader.read()
            retval, buffer = cv2.imencode('.jpg', frame, (cv2.IMWRITE_JPEG_QUALITY, 80))
            data = buffer.tobytes()
            base64_encoded = base64.b64encode(data).decode()
            self.publish("io.crossbar.demo.frames", base64_encoded, str(uuid.uuid4()))

        reader = AsyncFrameReader()
        reader.add_on_frame_listener(on_frame)
        reader.start()

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Connected:  {details}", details=details)
        yield threads.deferToThread(self.capture_and_send_frames)

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()


if __name__ == '__main__':
    session = ClientSession(wamp.ComponentConfig('realm1', {}))
    runner = wamp.ApplicationRunner('rs://localhost:8080', 'realm1')
    runner.run(session)
