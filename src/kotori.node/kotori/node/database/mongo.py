# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import txmongo
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet.interfaces import ILoggingContext
from twisted.python import log
from zope.interface.declarations import implementer

@implementer(ILoggingContext)
class MongoDatabaseService(ApplicationSession):
    """An application component for logging telemetry data to MongoDB databases"""

    #@inlineCallbacks
    #def __init__(self, config):
    #    ApplicationSession.__init__(self, config)

    def logPrefix(self):
        """
        Return a prefix matching the class name, to identify log messages
        related to this protocol instance.
        """
        return self.__class__.__name__

    @inlineCallbacks
    def onJoin(self, details):
        print("Realm joined (WAMP session started).")

        # subscribe to telemetry data channel
        self.subscribe(self.receive, u'de.elmyra.kotori.telemetry.data')

        self.startDatabase()

        #self.leave()

    @inlineCallbacks
    def startDatabase(self):
        #self.mongo = yield txmongo.MongoConnection(host='127.0.0.0', port=27017)
        self.mongo = yield txmongo.MongoConnection()

    def onLeave(self, details):
        print("Realm left (WAMP session ended).")

    def onDisconnect(self):
        print("Transport disconnected.")
        #reactor.stop()

    @inlineCallbacks
    def receive(self, data):
        #print "RECEIVE:", data

        # decode wire data
        payload = data.split(';')
        try:
            mma_x = int(payload[0])
            mma_y = int(payload[1])
            temp = float(payload[2])

            # store data to database
            if self.mongo:
                telemetry = self.mongo.kotori.telemetry
                yield telemetry.insert(dict(mma_x = mma_x, mma_y = mma_y, temp = temp))

        except ValueError:
            print('Could not decode data: {}'.format(data))


def boot_mongo_database(websocket_uri, debug=False):

    print 'INFO: Starting mongo database service, connecting to broker', websocket_uri

    runner = ApplicationRunner(websocket_uri, "kotori-realm", debug=False, debug_wamp=False, debug_app=False)
    runner.run(MongoDatabaseService, start_reactor=False)
