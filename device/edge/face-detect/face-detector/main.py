from os import path

from autobahn.twisted import wamp
import cv2
import numpy
from twisted.internet.defer import inlineCallbacks


class ClientSession(wamp.ApplicationSession):
    def detect_faces(self, data, uuid):
        image = numpy.fromstring(data, dtype=numpy.uint8)
        gray = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

        # Detect faces in the image
        faces = FACE_FASCADE.detectMultiScale(gray, scaleFactor=2)

        coords = list(list(map(int, face)) for face in faces)
        self.publish("io.crossbar.demo.faces", coords, uuid)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Connected:  {details}", details=details)
        self._transport.MAX_LENGTH = 1000000
        yield self.subscribe(self.detect_faces, "io.crossbar.demo.frames")

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()


if __name__ == '__main__':
    FACE_FASCADE = cv2.CascadeClassifier(
            path.join(path.dirname(path.realpath(__file__)), "cascades/haarcascade_frontalface_default.xml"))
    session = ClientSession(wamp.ComponentConfig('realm1', {}))
    runner = wamp.ApplicationRunner('rs://localhost:8080', 'realm1')
    runner.run(session)
