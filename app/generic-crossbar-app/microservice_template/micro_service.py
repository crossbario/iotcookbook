#!/usr/bin/env python3
import txaio
import argparse
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import RegisterOptions
from twisted.internet.defer import inlineCallbacks
from twisted.internet import ssl, reactor
from setproctitle import setproctitle
from utils.micro_service_config import MicroServiceConfig

CLIENT_CRT = 'certs/client_{}_crt.pem'
CLIENT_KEY = 'certs/client_{}_key.pem'


class ClientSession(ApplicationSession):
    """Class to handle connections to the router."""

    def __init__(self, *args, **kwargs):
        self.log.info('* microservice - initialise')
        self.conf = args[0].extra.get('conf')
        ApplicationSession.__init__(self, *args, **kwargs)

    def onConnect(self):
        self.log.info('* microservice - connect')
        self.join(self.conf.realm, [self.conf.mode], self.conf.user)

    def onDisconnect(self):
        self.log.info('* microservice - disconnect')

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('* microservice - onjoin')
        options = RegisterOptions(invoke='random')
        yield self.register(self.myrpc, 'hello.world.rpc', options)

        def test_rpc(params):
            self.call('hello.world.rpc', params)
            reactor.callLater(5, test_rpc, {'msg': 'REPEAT', 'from': self.conf.name})

        reactor.callLater(1, test_rpc, {'msg': 'HELLO'})

    def myrpc(self, params):
        self.log.info('{name} :: MyRPC called with params ({params})',
                      name=self.conf.name,
                      params=params)


if __name__ == '__main__':
    #
    #   We're going to read a minimal amount of startup from the commandd line, andd
    #   read our (relatively) complex configuration information froma prolfile (.ini file)
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('-p', '--profile', dest='profile', type=str, help='The name of the profile to use')
    args = parser.parse_args()
    setproctitle('xbr_application_{}'.format(args.profile))
    #
    #   We're supporting debug or info .. for a quiet life, switch 'info' for 'warning'
    #
    txaio.start_logging(level='debug' if args.debug else 'info')
    #
    #   This is just a wrapper for our configuration, the conf object is passed through
    #   to our service in the 'extra' parameter.
    #
    conf = MicroServiceConfig(args.profile if args.profile else 'micro_service.ini')
    #
    #   If you hit control+C, it tends to interrupt the retry cycle and generate an
    #   unsightly traceback, this just tidies that up a little.

    def orderlyShutdown():
        runner.log.info('* microservice - shutdown')
        runner.stop()

    reactor.addSystemEventTrigger('before', 'shutdown', orderlyShutdown)
    #
    #   This is our launcher, pretty standdard except we're loading in a specificate
    #   pre-generated client certificate.
    #
    runner = ApplicationRunner(
        url=conf.server_url,
        realm=conf.realm,
        ssl=ssl.DefaultOpenSSLContextFactory(
            privateKeyFileName=CLIENT_KEY.format(conf.name),
            certificateFileName=CLIENT_CRT.format(conf.name)
        ),
        extra={'conf': conf}
    )
    runner.run(ClientSession, auto_reconnect=True)
