# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
from kotori.configuration import configparser_to_dict
from kotori.errors import traceback_get_exception, last_error_and_traceback
from kotori.logger import startLogging
from twisted.logger import Logger
from twisted.internet import reactor
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from twisted.logger._levels import LogLevel

logger = Logger()

class WampSession(ApplicationSession):
    """
    Simple message publishing with Autobahn WebSockets.

    derived from:
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/basic/pubsub/basic/frontend.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/session/fromoutside/client.py
    """

    component = None

    def onJoin(self, details):
        logger.info("WAMP session joined: {}".format(details))
        try:
            if self.component:
                self.component(bus=self, config=self.config.extra)
        except Exception as ex:
            logger.error(last_error_and_traceback())

    def onDisconnect(self):
        logger.info("WAMP session disconnected")


class WampApplication(object):

    def __init__(self, url, realm=u'kotori', session_class=WampSession, config=None):
        """
        url: ws://master.example.com:9000/ws
        """
        self.url = url
        self.realm = realm
        self.session_class = session_class
        self.config = config

    def make(self):

        # connect to crossbar router/broker
        self.runner = ApplicationRunner(self.url, self.realm, extra=self.config)

        # run application session
        self.deferred = self.runner.run(self.session_class, start_reactor=False)

        def croak(ex, *args):
            logger.error('Problem in {name}, please check if "crossbar" WAMP broker is running. args={args}'.format(
                name=self.__class__.__name__, args=args))
            logger.error("{ex}, args={args!s}", ex=ex.getTraceback(), args=args)
            reactor.stop()
            raise ex

        self.deferred.addErrback(croak)


if __name__ == '__main__':
    startLogging(sys.stdout, level=LogLevel.levelWithName('debug'))
    app = WampApplication(url=u'ws://localhost:9000/ws')
    app.make()
    reactor.run()
