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
        self.conf.session = self
        self.log.info('* microservice - join on realm "{realm}"', realm=details.realm)
        options = RegisterOptions(invoke='roundrobin')
        yield self.register(self.authenticate_server, 'app.security.server.authenticate', options)
        yield self.register(self.authorize_server, 'app.security.server.authorize', options)

    def authorize_server(self, session, uri, action, options, details=None):
        self.log.debug('{name} :: Authorize authid=({authid}) uri=({uri}) action=({action})',
                      name=self.conf.name,
                      authid=session.get('authid'),
                      uri=uri,
                      action=action)

        logger_conf.session.call('app.logger.log_message', {
            'realm': self.conf.name,
            'type': 'authorize',
            'state': 'success',
            'authid': session.get('authid'),
            'uri': uri,
            'action': action
        })
        return {'allow': True, 'disclose': True}

    def authenticate_server(self, realm, authid, extra=None, details=None):

        def readme(dictionary, key):
            """wrap a dictionary lookup"""
            if key in dictionary:
                return dictionary[key]
            msg = '"{}" not found in dictionary for "{}"'.format(key, authid)
            raise ApplicationError('tls_error', msg)

        transport = readme(extra, 'transport')
        certificate = readme(transport, 'client_cert')
        sha1 = readme(certificate, 'sha1')

        common = certificate['subject']['cn']
        serial = certificate['serial']
        company = certificate['issuer']['ou']
        host = certificate['issuer']['cn']

        self.log.debug('{} :: Authenticate ({}) on realm ({}) with ({})'.format(
            self.conf.name,
            authid,
            realm,
            sha1
        ))
        logger_conf.session.call('app.logger.log_message', {
            'realm': self.conf.name,
            'type': 'authenticate',
            'state': 'success',
            'authid': authid,
            'cn': common,
            'host': host
        })
        return {'role': 'server'}


if __name__ == '__main__':
    #
    #   We're going to read a minimal amount of startup from the commandd line, andd
    #   read our (relatively) complex configuration information froma prolfile (.ini file)
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('-p', '--profile', dest='profile', type=str, help='The name of the profile to use')
    args = parser.parse_args()
    setproctitle('xbr_auth_{}'.format(args.profile))
    #
    #   We're supporting debug or info .. for a quiet life, switch 'info' for 'warning'
    #
    txaio.start_logging(level='debug' if args.debug else 'info')
    #
    #   This is just a wrapper for our configuration, the conf object is passed through
    #   to our service in the 'extra' parameter.
    #
    auth_conf = MicroServiceConfig(args.profile, 'auth')
    logger_conf = MicroServiceConfig(args.profile, 'logger')
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
    logger.run(ClientSession, False, auto_reconnect=True)
    #
    #   This is our connection to the crossbar realm which is to be used for
    #   normal application communications.

    auth = ApplicationRunner(
        url=auth_conf.server_url,
        realm=auth_conf.realm,
        ssl=ssl.DefaultOpenSSLContextFactory(
            privateKeyFileName=CLIENT_KEY.format(auth_conf.name),
            certificateFileName=CLIENT_CRT.format(auth_conf.name)
        ),
        extra={'conf': auth_conf}
    )
    #
    #   If you hit control+C, it tends to interrupt the retry cycle and generate an
    #   unsightly traceback, this just tidies that up a little.

    def orderlyShutdown():
        logger.log.info('* microservice - shutdown logger and auth')
        logger.stop()
        auth.stop()

    reactor.addSystemEventTrigger('before', 'shutdown', orderlyShutdown)
    auth.run(ClientSession, auto_reconnect=True)
