import os
import argparse

import six

import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning

from autobahn.util import utcnow
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError


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


import rtmidi

class LaunchpadComponent(ApplicationSession):
    """
    Our component wrapping a Novation Launchpad USB controller.
    """

    @inlineCallbacks
    def onJoin(self, details):
        """
        Callback when the WAMP session has been established and is ready for use.
        """

        # get the Pi serial number
        self._serial = get_serial()

        # all procedures/events will have this URI prefix
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.launchpad'.format(self._serial)

        # print startup infos
        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("LaunchpadComponent connected: {details}", details=details)

        # get component user extra configuration
        cfg = self.config.extra

        midiout = rtmidi.MidiOut()
        available_ports = midiout.get_ports()
        launchpad_port=None
        i = 0
        for port in available_ports:
            if port.startswith('Launchpad'):
                launchpad_port = i
                break
            else:
                i += 1

        if launchpad_port:
            self.log.info('Launchpad port: {launchpad_port}', launchpad_port=launchpad_port)
            port = midiout.open_port(launchpad_port)
            self.log.info('port: {}'.format(port))

            self._midiIn = port
            self._midiOut = port
            self._drumrackMode = False

        else:
            self.log.warn('No Launchpad on any port found! Available ports: {available_ports}', available_ports=available_ports)

        # register procedures
        for proc in [
            (self.started, u'started'),
            (self.reset, u'reset'),
            (self.setDrumRackMode, u'set_drumrack_mode'),
            (self.light, u'light'),
            (self.lightAll, u'light_all'),
            (self.lightAllTest, u'light_all_test'),
            (self.lightSingleTest, u'light_single_test'),
        ]:
            uri = u'{}.{}'.format(self._prefix, proc[1])
            yield self.register(proc[0], uri)
            self.log.info('registered procedure {uri}', uri=uri)

        self._is_ready = True
        self.log.info("LaunchpadComponent ready!")

    def reset(self):
        self._midiOut.send_message([0xb0, 0, 0])
        self._drumrackMode = False

    def setDrumRackMode(self, drumrack=True):
        self._drumrackMode = drumrack
        self._midiOut.send_message([0xb0, 0, drumrack and 2 or 1])

    def light(self, x, y, red, green):
        if not 0 <= x <= 8: return
        if not 0 <= y <= 8: return
        if not 0 <= red <= 3: return
        if not 0 <= green <= 3: return

        #if not 0 <= x <= 8: raise LaunchPadError("Bad x value %s" % x)
        #if not 0 <= y <= 8: raise LaunchPadError("Bad y value %s" % y)
        #if not 0 <= red <= 3: raise LaunchPadError("Bad red value %s" % red)
        #if not 0 <= green <= 3: raise LaunchPadError("Bad green value %s" % green)

        velocity = 16*green + red + 8 + 4

        if y==8:
            if x != 8:
                note = 104 + x
                self._midiOut.send_message([0xb0,note,velocity])
            return

        if self._drumrackMode:
            if x==8:
                # Last column runs from 100 - 107
                note = 107-y;
            elif x<4:
                note = 36 + x + 4*y
            else:
                # Second half starts at 68, but x will start at 4
                note = 64 + x + 4*y
        else:
            note = x + 16*(7-y)

        self._midiOut.send_message([0x90,note,velocity])

    def lightAll(self, levels):
        velocity = 0
        for level in self._orderAll(levels):
            red = level[0]
            green = level[1]
            if velocity:
                velocity2 = 16*green + red + 8 + 4
                self._midiOut.send_message([0x92, velocity, velocity2])
                velocity = 0
            else:
                velocity = 16*green + red + 8 + 4
        self.light(0,0,levels[0][0][0],levels[0][0][1])

    def _orderAll(self,levels):
        for y in range(8):
            for x in range(8):
                yield levels[x][7-y]
        x = 8
        for y in range(8):
            yield levels[x][7-y]
        y = 8
        for x in range(8):
            yield levels[x][y]

    def lightSingleTest(self):
        for x in range(8):
            for y in range(8):
                self.light(x,y,x%4,y%4)

    def lightAllTest(self,r=None,g=None):
        grid = []
        for x in range(9):
            grid.append([])
            for y in range(9):
                if (r==None):
                    grid[x].append( (x%4, y%4) )
                else:
                    grid[x].append( (r%4, g%4) )

        self.lightAll(grid)

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
    parser.add_argument('--url', dest='url', type=six.text_type, default=url, help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=realm, help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # custom configuration data
    extra = {
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(LaunchpadComponent, auto_reconnect=True)
