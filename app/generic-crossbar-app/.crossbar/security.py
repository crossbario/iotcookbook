"""main module for crossbar_io application"""
#
#    This module is Auto-generated, please do not edit.
#
import txaio
from twisted.internet.defer import inlineCallbacks
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


class Crossbar(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        
        txaio.start_logging(level='info')

        soptions = SubscribeOptions()
        roptions = RegisterOptions(details_arg='details')
        #
        #   Register our Authorizers
        #
        yield self.register(self.authorize_client, 'xbr.security.authorize_client', roptions)
        yield self.register(self.authorize_server, 'xbr.security.authorize_server', roptions)
        #
        #   Register our Authenticatrs
        #
        yield self.register(self.authenticate_client, 'xbr.security.authenticate_client', roptions)
        yield self.register(self.authenticate_server, 'xbr.security.authenticate_server', roptions)
    #
    #   Authorization

    def authorize_server(self, session, uri, action, options, details=None):
        return {'allow': True, 'disclose': True}

    def authorize_client(self, session, uri, action, options, details=None):
        return {'allow': True, 'disclose': True}
    #
    #   Authentication

    def authenticate_client(self, realm, authid, extra=None, details=None):
        return {'role': 'client'}

    def authenticate_server(self, realm, authid, extra=None, details=None):
        def readme(dictionary, key):
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

        self.log.info('+ "{authid}" on realm "{realm}" CN="{common}" COMPANY="{company}" SHA="{sha1}"',
                      authid=authid,
                      realm=realm,
                      common=common,
                      company=company,
                      sha1=sha1)
        return {'role': 'authenticator'}
