import base64
from os import path

from autobahn.twisted import wamp
import cv2
import numpy
from twisted.internet.defer import inlineCallbacks


class ClientSession(wamp.ApplicationSession):
    def detect_faces(self, data, uuid):
        data = base64.b64decode(data)
        image = numpy.fromstring(data, dtype=numpy.uint8)
        image_np = cv2.imdecode(image, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = FACE_FASCADE.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)
        coords = [dict(zip(('x', 'y', 'w', 'h'), map(int, face))) for face in faces]
        self.publish("io.crossbar.demo.faces", coords, uuid)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Connected:  {details}", details=details)
        yield self.subscribe(self.detect_faces, "io.crossbar.demo.frames")

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()


if __name__ == '__main__':
    FACE_FASCADE = cv2.CascadeClassifier(
            path.join(path.dirname(path.realpath(__file__)), "cascades/haarcascade_frontalface_default.xml"))
    session = ClientSession(wamp.ComponentConfig('realm1', {}))
    runner = wamp.ApplicationRunner('ws://localhost:8080/ws', 'realm1')
    runner.run(session)
