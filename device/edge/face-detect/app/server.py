from os import environ, path
import multiprocessing

import cv2
import numpy

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import RegisterOptions
from twisted.internet.defer import inlineCallbacks
from twisted.internet import threads, reactor


class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print('Joined session={}'.format(details.realm))
        options = RegisterOptions(concurrency=MAX_CONCURRENT_TASKS, invoke='roundrobin')
        yield self.register(self.face_detect_caller, "io.crossbar.demo.cvengine.detect_faces", options)

    def face_detect_caller(self, image_data):
        return threads.deferToThread(self.get_faces_coordinates, image_data)

    def get_faces_coordinates(self, image_data):
        # Create the haar cascade
        face_cascade = cv2.CascadeClassifier(
            path.join(path.dirname(path.realpath(__file__)),
                      "cascades/haarcascade_frontalface_default.xml"))

        image = numpy.fromstring(image_data, dtype=numpy.uint8)
        image_np = cv2.imdecode(image, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
        return [{'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)} for (x, y, w, h) in faces]


if __name__ == '__main__':
    runner = ApplicationRunner(environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://localhost:8080/ws"),
                               environ.get("AUTOBAHN_DEMO_REALM", u"realm1"))
    MAX_CONCURRENT_TASKS = int(environ.get('AUTOBAHN_DEMO_CPU_COUNT', multiprocessing.cpu_count()))
    reactor.suggestThreadPoolSize(MAX_CONCURRENT_TASKS)
    runner.run(MyComponent, auto_reconnect=True)
