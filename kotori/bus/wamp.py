# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.logger import Logger
from twisted.python.failure import Failure
from autobahn.twisted.wamp import ApplicationRunner

log = Logger()

class WampBus(object):

    def __init__(self, uri=None, application_factory=None, session_factory=None):
        self.uri = uri
        self.application_factory = application_factory or self.application_factory
        self.session_factory = session_factory

    def connect(self):

        # Connect to crossbar router/broker
        self.runner = self.application_factory()

        # Pass session factory to Wamp application runner
        d = self.runner.run(self.session_factory, start_reactor=False)
        d.addErrback(self.on_error)

    def application_factory(self):
        # TODO: Obtain the realm from outside
        return ApplicationRunner(self.uri, u'kotori-realm')

    def on_error(self, ex, *args, **kwargs):
        log.failure(u'Problem starting {name}, please also check if WAMP broker '
                    u'"crossbar" is running at {uri}. args={args!s}, kwargs={kwargs!s}', failure=ex,
            name=self.__class__.__name__, uri=self.uri, args=args, kwargs=kwargs)


class WampSessionMixin(object):
    def onUserError(self, ex, msg):
        """
        Override of wamp.ApplicationSession
        """
        # Handle exception and print to the logs
        log.failure(msg, failure=Failure(ex))
