import os
import re
import sys
import argparse

import six

import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet import stdio
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.error import ReactorNotRunning

from autobahn.util import utcnow
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError


class XboxdrvReceiver(LineReceiver):
    """
    Protocol for parsing output from Xboxdrv.
    """
    log = txaio.make_logger()

    delimiter = b'\n'

    def __init__(self):
        self._session = None
        self._last = None

    def connectionMade(self):
        self.log.info('XboxdrvReceiver connected')

    def lineReceived(self, line):
        self.log.debug("XboxdrvReceiver line received: {line}", line=line)

        # Parse lines received from Xboxdrv. Lines look like:
        # X1:  -764 Y1:  4198  X2:   385 Y2:  3898  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
        try:
            _line = line.decode('ascii')
            parts = re.split(r'[:\s]+', _line)
            data = {}
            for i in range(0, len(parts) - 2, 2):
                attr = parts[i]
                val = parts[i + 1]
                data[attr] = int(val)
        except:
            self.log.error("XboxdrvReceiver: could not parse line: {line}", line=line)
            self.log.failure()
        else:
            # determine change set
            changed = {}
            if self._last:
                for k in data:
                    if data[k] != self._last[k]:
                        changed[k] = data[k]
            else:
                changed = data

            # if WAMP session is active and change set is non-empty,
            # forward the controller data to the WAMP session
            if len(changed):
                self.log.info("XboxdrvReceiver event data: {changed}", changed=changed)
                if self._session:
                    self._session.on_data(data)
                self._last = data


def get_serial():
    """
    Get the Pi's serial number.
    """
    with open('/proc/cpuinfo') as fd:
        for line in fd.read().splitlines():
            line = line.strip()
            if line.startswith('Serial'):
                _, serial = line.split(':')
                return serial.strip().lstrip('0')


class XboxControllerAdapter(ApplicationSession):
    """
    Our component wrapping the buzzer hardware.
    """

    @inlineCallbacks
    def onJoin(self, details):
        """
        Callback when the WAMP session has been established and is ready for use.
        """

        # get component user extra configuration
        cfg = self.config.extra

        # get the device ID
        self._serial = cfg[u'id']

        # all procedures/events will have this URI prefix
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.gamepad'.format(self._serial)

        # print startup infos
        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("XboxControllerAdapter connected: {details}", details=details)

        # register procedures
        for proc in [
            (self.started, u'started'),
        ]:
            uri = u'{}.{}'.format(self._prefix, proc[1])
            yield self.register(proc[0], uri)
            self.log.info('registered procedure {uri}', uri=uri)

        # remember startup timestamp
        self._started = utcnow()

        self.log.info("XboxControllerAdapter ready!")

    def started(self):
        """
        Get UTC timestamp when the component started.

        :returns: ISO8601 formatted UTC timestamp when the component started.
        :rtype: str
        """
        return self._started

    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    # Crossbar.io connection configuration
    url = os.environ.get('CBURL', u'wss://demo.crossbar.io/ws')
    realm = os.environ.get('CBREALM', u'crossbardemo')

    # parse command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument("--id", dest='id', type=six.text_type, default=None, help='The Device ID to use. Default is to use the Raspberry Pi Serial Number')
    parser.add_argument('--url', dest='url', type=six.text_type, default=url, help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=realm, help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # used to receive and parse data from Xboxdrv
    xbox = XboxdrvReceiver()
    stdio.StandardIO(xbox)

    # custom configuration data
    extra = {
        # device ID
        u'id': args.id,

        # our WAMP component needs access to the Xboxdrv receiver
        u'xbox': xbox
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(XboxControllerAdapter, auto_reconnect=True)
