import asyncio
from os import environ, path

import cv2
import numpy

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


def get_faces_coordinates(image_data):
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


class MyComponent(ApplicationSession):
    async def onJoin(self, details):
        print('Joined session={}'.format(details.realm))
        await self.register(get_faces_coordinates, "io.crossbar.demo.cvengine.detect_faces")

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    runner = ApplicationRunner(environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://localhost:8080/ws"),
                               environ.get("AUTOBAHN_DEMO_REALM", u"realm1"))
    runner.run(MyComponent)
