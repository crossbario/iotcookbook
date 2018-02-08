import argparse
from os import environ, path
import sys
import tempfile

import cv2
import numpy

from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def main(reactor, session):
    with open(photo, 'rb') as f:
        data = f.read()
    faces = yield session.call("io.crossbar.demo.cvengine.detect_faces", data)
    image_raw = numpy.fromstring(data, dtype=numpy.uint8)
    image_np = cv2.imdecode(image_raw, cv2.IMREAD_COLOR)
    for f in faces:
        cv2.rectangle(image_np, (f['x'], f['y']), (f['x'] + f['w'], f['y'] + f['h']), (0, 255, 0), 2)
    cv2.imwrite(tempfile.mktemp('.jpg', 'fd_', dir='.'), image_np)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    photo = path.abspath(path.expanduser(args.file))
    if not path.exists(photo):
        print('File "{}" does not exist'.format(photo))
        sys.exit(1)

    transport = {
        "type": "rawsocket",
        "url": "ws://localhost/ws",
        "endpoint": UNIXClientEndpoint(reactor, "/home/om26er/crossbar.sock"),
        "serializer": "msgpack"
    }

    component = Component(main=main, transports=[transport], realm=environ.get("AUTOBAHN_DEMO_REALM", u"realm1"))
    run([component])
