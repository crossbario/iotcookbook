import os
import argparse

import six

import txaio
txaio.use_twisted()

import RPi.GPIO as GPIO

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


class BuzzerComponent(ApplicationSession):
    """
    Our component wrapping the buzzer hardware.
    """

    @inlineCallbacks
    def onJoin(self, details):
        """
        Callback when the WAMP session has been established and is ready for use.
        """

        # get the Pi serial number
        self._serial = get_serial()

        # all procedures/events will have this URI prefix
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.buzzer'.format(self._serial)

        # print startup infos
        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("BuzzerComponent connected: {details}", details=details)

        # get component user extra configuration
        cfg = self.config.extra

        # initialize buzzer
        self._buzzer_pin = cfg['buzzer_pin']
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._buzzer_pin, GPIO.OUT)
        GPIO.output(self._buzzer_pin, 0)

        # remember startup timestamp
        self._started = utcnow()

        # flag indicating if the beeper is already operating
        self._is_beeping = False

        # register procedures
        for proc in [
            (self.started, u'started'),
            (self.is_beeping, u'is_beeping'),
            (self.beep, u'beep'),
            (self.welcome, u'welcome'),
        ]:
            uri = u'{}.{}'.format(self._prefix, proc[1])
            yield self.register(proc[0], uri)
            self.log.info('registered procedure {uri}', uri=uri)

        self._is_ready = True
        self.log.info("BuzzerComponent ready!")

        # play annoying welcome beeps to give acoustic feedback for being ready
        self.welcome()

    def started(self):
        """
        Get UTC timestamp when the component started.

        :returns: ISO8601 formatted UTC timestamp when the component started.
        :rtype: str
        """
        return self._started

    def is_beeping(self):
        """
        Check if the buzzer is currently playing a beeping sequence, and hence a (further)
        concurrent call to beep() will fail.

        :returns: Flag indicating whether the buzzer is currently beeping.
        :rtype: bool
        """
        return self._is_beeping

    @inlineCallbacks
    def beep(self, count=None, on=None, off=None):
        """
        Trigger beeping sequence.

        :param count: Number of beeps.
        :type count: int

        :param on: ON duration in ms.
        :type on: int

        :param off: OFF duration in ms.
        :type off: int
        """
        # use default values
        count = count or 1
        on = on or 30
        off = off or 80

        # check types
        if type(count) not in six.integer_types:
            raise TypeError('"count" must be an integer')
        if type(on) not in six.integer_types:
            raise TypeError('"on" must be an integer')
        if type(off) not in six.integer_types:
            raise TypeError('"off" must be an integer')

        if self._is_beeping:
            raise ApplicationError(u'{}.already-beeping'.format(self._prefix), 'currently already in a beeping sequence')

        # run the beeping sequence ..
        self.log.info('start beeping sequence: count={count}, on={on}, off={off}', count=count, on=on, off=off)

        self._is_beeping = True
        self.publish(u'{}.on_beep_started'.format(self._prefix), count=count, on=on, off=off)

        for i in range(count):
            GPIO.output(self._buzzer_pin, 1)
            yield sleep(float(on) / 1000.)
            GPIO.output(self._buzzer_pin, 0)
            yield sleep(float(off) / 1000.)

        self._is_beeping = False
        self.publish(u'{}.on_beep_ended'.format(self._prefix))

    @inlineCallbacks
    def welcome(self):
        """
        Play annoying beep sequence.
        """
        self.log.info('start welcome beep sequence ..')

        # sequence of 7 short beeps
        yield self.beep(7)

        # wait 0.5s
        yield sleep(.5)

        # another 3 longer beeps
        yield self.beep(3, on=200, off=200)

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
        # GPI pin of buzzer
        u'buzzer_pin': 16,
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(BuzzerComponent, auto_reconnect=True)
