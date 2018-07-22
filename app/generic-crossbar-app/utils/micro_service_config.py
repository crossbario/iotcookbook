from configparser import RawConfigParser

PROPERTIES = [
    ('debug', False),
    ('user', 'none'),
    ('realm', 'none'),
    ('logger', 'none'),
    ('host', 'localhost'),
    ('port', '8080'),
    ('ssl', 'true'),
    ('name', 'no_node'),
    ('mode', 'tls'),
    ('desc', 'Generic Microservice Name')
]

PROTOCOLS = {
    True: 'wss',
    False: 'ws'
}


class MicroServiceConfig(object):
    """routines to deal with INI file settings"""

    @property
    def is_ssl(self):
        """convers the SSL setting into a boolean"""
        if self._ssl.lower() in ['yes', 'true']:
            return True
        return False

    @property
    def proto(self):
        """return the WS protocol string depending on the SSL setting"""
        return PROTOCOLS[self.is_ssl]

    @property
    def server_url(self):
        """return a complete connect URL for the server"""
        return "%s://%s:%s/ws" % (self.proto, self.host, self.port)

    def pget(self, attr_name):
        """custom property getter"""
        def fget(self):
            """get"""
            return getattr(self, '_'+attr_name)
        return fget

    def pset(self, attr_name):
        """custom property setter"""
        def fset(self, value):
            """set"""
            setattr(self, '_'+attr_name, value)
        return fset

    def __init__(self, filename, section='global'):
        """set things up"""
        parser = RawConfigParser()
        parser.read(filename)
        self.__parser = parser
        for attr_name, default in PROPERTIES:
            value = parser.get(section, attr_name, fallback=default)
            setattr(self, '_'+attr_name, value)
            setattr(self.__class__, attr_name, property(self.pget(attr_name), self.pset(attr_name)))
