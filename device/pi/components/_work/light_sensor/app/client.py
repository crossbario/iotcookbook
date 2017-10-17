#!/usr/bin/python

from threading import current_thread
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning

from autobahn.util import utcnow
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError

import RPi.GPIO as GPIO


import os
import argparse

import six

import txaio
txaio.use_twisted()

# OK
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

# probably
def config_light_sensor_gpio(channel):
    """
    configure the Light Sensor GPIO Pin
    """

    GPIO.setmode(GPIO.BOARD)

    # declare GPIO Pin as input and enable the pull-up resistor
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class LightSensorComponent(ApplicationSession):
    """Our component wrapping a light sensor for threshold triggering."""

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('Session joined on thread {thread_id}: {details}', thread_id=current_thread().ident, details=details)

        """Callback when the WAMP session has been established and is ready for use."""
        # get the Pi serial number
        self._serial = get_serial()

        # all procedures/events will have this URI prefix
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.light_sensor'.format(self._serial)

        # print startup infos
        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("LightSensorComponent connected: {details}", details=details)

        # get component user extra configuration
        cfg = self.config.extra

        # initialize button
        self._light_sensor_pin = cfg['light_sensor_pin']
        GPIO.setwarnings(False)
        config_light_sensor_gpio(self._light_sensor_pin)

        # setup edge detection for the light sensor
        GPIO.add_event_detect(self._light_sensor_pin, GPIO.RISING, callback=self.light_change)

        # remember startup timestamp
        self._started = utcnow()

        # flag indicating if the button is already pressed
        self._is_dark = False

        # register procedures
        for proc in [
            (self.started, u'started'),
            (self._is_pressed, u'is_dark'),
            # (self.press, u'press'),
        ]:
            uri = u'{}.{}'.format(self._prefix, proc[1])
            yield self.register(proc[0], uri)
            self.log.info('registered procedure {uri}', uri=uri)

        self._is_ready = True
        self.log.info("LightSensorComponent ready!")

    def started(self):
        """
        Get UTC timestamp when the component started.

        :returns: ISO8601 formatted UTC timestamp when the component started.
        :rtype: str
        """
        return self._started

    def is_dark(self):
        """
        Check if the buzzer is currently playing a beeping sequence, and hence a (further)
        concurrent call to beep() will fail.

        :returns: Flag indicating whether the buzzer is currently beeping.
        :rtype: bool
        """
        return self._is_dark

    def light_change(self, portnr=1000):
        """is called by the edge detection and running in a new thread
            calls the _press() method which performs the action triggered by the button """
        self.log.info('GPIO edge callback on thread {thread_id}', thread_id=current_thread().ident)
        reactor.callFromThread(self._light_change)

    @inlineCallbacks
    def _light_change(self):
        """light sensor edge event handler"""

        self.log.info('Light sensor edge event handler on thread {thread_id}', thread_id=current_thread().ident)

        # """ if the button is pressed during the progress is running this Error will be fired"""
        # if self._is_pressed:
        #     raise ApplicationError(u'{}.already-pressed'.format(self._prefix), 'Button is already pressed ')
        #
        # self._is_pressed = True
        # self.log.info("Pressed")
        #
        # """ publish event button_pressed"""
        # self.publish(u'{}.button_pressed'.format(self._prefix))
        #
        # """wait for a short time"""
        # yield sleep(1000 / 1000.)
        #
        # self._is_pressed = False
        # """ publish event button_released"""
        # self.publish(u'{}.button_released'.format(self._prefix))
        #
        # self.log.info("released")

    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.disconnect()
        GPIO.output(15, GPIO.LOW)
        GPIO.cleanup()

    def onDisconnect(self):
        self.log.info("connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    # Crossbar.io connection configuration

    url = os.environ.get('CBURL', u'wss://demo.crossbar.io/ws')
    # url = os.environ.get('CBURL', u'192.168.1.142')
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
        u'light_sensor_pin': 15,
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(LightSensorComponent, auto_reconnect=True)
