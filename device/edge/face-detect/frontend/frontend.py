import asyncio
import argparse
from os import environ, path
import sys
import tempfile

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import cv2
import numpy


class MyComponent(ApplicationSession):
    async def onJoin(self, details):
        with open(photo, 'rb') as f:
            data = f.read()
        faces = await self.call("io.crossbar.demo.cvengine.detect_faces", data)
        image_raw = numpy.fromstring(data, dtype=numpy.uint8)
        image_np = cv2.imdecode(image_raw, cv2.IMREAD_COLOR)
        for f in faces:
            cv2.rectangle(image_np, (f['x'], f['y']), (f['x'] + f['w'], f['y'] + f['h']),
                          (0, 255, 0), 2)
        cv2.imwrite(tempfile.mktemp('.jpg', 'fd_', dir='.'), image_np)
        self.leave()

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    photo = path.abspath(path.expanduser(args.file))
    if not path.exists(photo):
        print('File "{}" does not exist'.format(photo))
        sys.exit(1)
    runner = ApplicationRunner(environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://localhost:8080/ws"),
                               environ.get("AUTOBAHN_DEMO_REALM", u"realm1"))
    runner.run(MyComponent)
