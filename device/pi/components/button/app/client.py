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


def config_button_gpio(channel):
    """
    configure the Button GPIO Pin
    """

    GPIO.setmode(GPIO.BCM)

    # declare GPIO Pin as input and enable the pull-up resistor
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def config_LED_gpio(LED_pin):

    """
    configure the LED - GPIO Pin
    """
    GPIO.setmode(GPIO.BCM)

    # declare GPIO Pin as output
    GPIO.setup(LED_pin, GPIO.OUT)


class ButtonComponent(ApplicationSession):
    """Our component wrapping a Button with edge detection."""

    LED_status = False

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('Session joined on thread {thread_id}: {details}', thread_id=current_thread().ident, details=details)

        LED_pin = 15

        self.LED_status = False
        """Callback when the WAMP session has been established and is ready for use."""
        # get the Pi serial number
        self._serial = get_serial()

        # all procedures/events will have this URI prefix
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.button'.format(self._serial)

        # print startup infos
        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("ButtonComponent connected: {details}", details=details)

        # get component user extra configuration
        cfg = self.config.extra

        # initialize button
        self._button_pin = cfg['button_pin']
        GPIO.setwarnings(False)
        # config_button_gpio(_button_pin)
        config_button_gpio(18)
        GPIO.add_event_detect(18, GPIO.FALLING, callback=self.press, bouncetime=250)

        # initialize LED
        config_LED_gpio(LED_pin)

        # remember startup timestamp
        self._started = utcnow()

        # flag indicating if the button is already pressed
        self._is_pressed = False

        # register procedures
        for proc in [
            (self.started, u'started'),
            (self._is_pressed, u'is_pressed'),
            (self.press, u'press'),
            (self.led_on, u'led_on'),
            (self.led_off, u'led_off')
        ]:
            uri = u'{}.{}'.format(self._prefix, proc[1])
            yield self.register(proc[0], uri)
            self.log.info('registered procedure {uri}', uri=uri)

        self._is_ready = True
        self.log.info("ButtonComponent ready!")

    def started(self):
        """
        Get UTC timestamp when the component started.

        :returns: ISO8601 formatted UTC timestamp when the component started.
        :rtype: str
        """
        return self._started

    def is_pressed(self):
        """
        Check if the buzzer is currently playing a beeping sequence, and hence a (further)
        concurrent call to beep() will fail.

        :returns: Flag indicating whether the buzzer is currently beeping.
        :rtype: bool
        """
        return self._is_pressed

    def get_status(self):

        return self.LED_status

    def set_status(self, status):

        self.LED_status = status
        # self.log.info(self.get_status())
        return 0

    def press(self, portnr=1000):
        """is called by the edge detection and running in a new thread
            calls the _press() method which performs the action triggered by the button """
        self.log.info('GPIO edge callback on thread {thread_id}', thread_id=current_thread().ident)
        reactor.callFromThread(self._press)

    @inlineCallbacks
    def _press(self):
        """button pressed handler"""

        self.log.info('Button pressed handler on thread {thread_id}', thread_id=current_thread().ident)

        """ if the button is pressed during the progress is running this Error will be fired"""
        if self._is_pressed:
            raise ApplicationError(u'{}.already-pressed'.format(self._prefix), 'Button is already pressed ')

        self._is_pressed = True
        self.log.info("Pressed")

        """ publish event button_pressed"""
        self.publish(u'{}.button_pressed'.format(self._prefix))

        """wait for a short time"""
        yield sleep(1000 / 1000.)

        self._is_pressed = False
        """ publish event button_released"""
        self.publish(u'{}.button_released'.format(self._prefix))

        self.log.info("released")

    @inlineCallbacks
    def led_on(self, LED_pin=15):
        """ callback function to put LED GPIO high => LED on"""
        if self.get_status() is False:
            GPIO.output(LED_pin, GPIO.HIGH)
            self.publish(u'{}.LED_on'.format(self._prefix))
            self.log.info("LED_on")
            self.set_status(True)

        yield sleep(1 / 1000.)

    @inlineCallbacks
    def led_off(self, LED_pin=15):
        """ callback function to put LED GPIO low => LED off """
        if self.get_status() is True:
            GPIO.output(LED_pin, GPIO.LOW)
            self.publish(u'{}.LED_off'.format(self._prefix))
            self.log.info("LED_off")
            self.set_status(False)

        yield sleep(1 / 1000.)

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
        u'button_pin': 18,
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(ButtonComponent, auto_reconnect=True)
