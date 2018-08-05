from os import environ, path
import multiprocessing

import cv2
import numpy

from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from autobahn.wamp import RegisterOptions
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import threads, reactor

transport = {
    "type": "rawsocket",
    "url": "ws://localhost/ws",
    "endpoint": UNIXClientEndpoint(reactor, "/home/om26er/crossbar.sock"),
    "serializer": "msgpack"
}

component = Component(transports=[transport], realm=environ.get("AUTOBAHN_DEMO_REALM", u"realm1"))


@inlineCallbacks
def on_join(session, details):
    print('Joined session={}'.format(details.realm))
    reactor.suggestThreadPoolSize(MAX_CONCURRENT_TASKS)
    options = RegisterOptions(concurrency=MAX_CONCURRENT_TASKS, invoke='roundrobin')
    yield session.register(get_faces_coordinates, "io.crossbar.demo.cvengine.detect_faces", options)


@inlineCallbacks
def get_faces_coordinates(image_data):
    def actually_get_face_coordinates(data):
        image = numpy.fromstring(data, dtype=numpy.uint8)
        image_np = cv2.imdecode(image, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = FACE_FASCADE.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
        return [dict(zip(('x', 'y', 'w', 'h'), map(int, face))) for face in faces]

    res = yield threads.deferToThread(actually_get_face_coordinates, image_data)
    returnValue(res)


if __name__ == '__main__':
    MAX_CONCURRENT_TASKS = int(environ.get('AUTOBAHN_DEMO_CPU_COUNT', multiprocessing.cpu_count()))
    FACE_FASCADE = cv2.CascadeClassifier(
            path.join(path.dirname(path.realpath(__file__)), "cascades/haarcascade_frontalface_default.xml"))
    run([component])
