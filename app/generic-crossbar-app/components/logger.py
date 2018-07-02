#!/usr/bin/env python3
import txaio
import argparse
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import RegisterOptions
from twisted.internet import ssl, reactor
from twisted.internet.defer import inlineCallbacks
from setproctitle import setproctitle
from utils.micro_service_config import MicroServiceConfig
from autobahn.wamp.exception import ApplicationError

CLIENT_CRT = 'certs/client_{}_crt.pem'
CLIENT_KEY = 'certs/client_{}_key.pem'


class ClientSession(ApplicationSession):
    """Class to handle connections to the router."""

    def __init__(self, *args, **kwargs):
        self.conf = args[0].extra.get('conf')
        ApplicationSession.__init__(self, *args, **kwargs)

    def onConnect(self):
        self.log.info('* microservice - connect to realm "{realm}"', realm=self.conf.realm)
        self.join(self.conf.realm, [self.conf.mode], self.conf.user)

    def onDisconnect(self, *args, **kwargs):
        self.log.info('* microservice - disconnect from realm "{realm}"', realm=self.conf.realm)

    def onLeave(self, *args, **kwargs):
        self.log.info('* microservice - leave realm "{realm}"', realm=self.conf.realm)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('* microservice - join on realm "{realm}"', realm=details.realm)
        options = RegisterOptions(invoke='roundrobin')
        yield self.register(self.log_message, 'app.logger.log_message', options)
        yield self.subscribe(self.log_login, 'wamp.session.on_join')
        yield self.subscribe(self.log_leave, 'wamp.session.on_leave')

    def log_message(self, message):
        self.log.info('> Message={message}', message=message)

    def log_login(self, details):
        message = {
            'session': details.get('session'),
            'type': 'login',
            'authid': details.get('authid'),
            'authrole': details.get('authrole'),
            'ip': details.get('transport', {}).get('peer'),
            'sha1': details.get('transport').get('client_cert').get('sha1')
        }
        self.log.info('> Message={message}', message=message)

    def log_leave(self, details):
        message = {
            'session': details,
            'type': 'leave'
        }
        self.log.info('> Message={message}', message=message)


if __name__ == '__main__':
    #
    #   We're going to read a minimal amount of startup from the commandd line, andd
    #   read our (relatively) complex configuration information froma prolfile (.ini file)
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('-p', '--profile', dest='profile', type=str, help='The name of the profile to use')
    args = parser.parse_args()
    setproctitle('xbr_logger_{}'.format(args.profile))
    #
    #   We're supporting debug or info .. for a quiet life, switch 'info' for 'warning'
    #
    txaio.start_logging(level='debug' if args.debug else 'info')
    #
    #   This is just a wrapper for our configuration, the conf object is passed through
    #   to our service in the 'extra' parameter.

    logger_conf = MicroServiceConfig(args.profile)

    #
    #   If you hit control+C, it tends to interrupt the retry cycle and generate an
    #   unsightly traceback, this just tidies that up a little.

    def orderlyShutdown():
        logger.log.info('* microservice - shutdown logger')
        logger.stop()

    #
    #   This is our connection to the logging realm for infrastructure traffic that
    #   should be partitioned off from application traffic.

    logger = ApplicationRunner(
        url=logger_conf.server_url,
        realm=logger_conf.realm,
        ssl=ssl.DefaultOpenSSLContextFactory(
            privateKeyFileName=CLIENT_KEY.format(logger_conf.name),
            certificateFileName=CLIENT_CRT.format(logger_conf.name)
        ),
        extra={'conf': logger_conf}
    )
    reactor.addSystemEventTrigger('before', 'shutdown', orderlyShutdown)
    logger.run(ClientSession, auto_reconnect=True)
