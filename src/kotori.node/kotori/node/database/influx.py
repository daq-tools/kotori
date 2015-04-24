# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from influxdb.influxdb08 import InfluxDBClient
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet.interfaces import ILoggingContext
from twisted.python import log
from zope.interface.declarations import implementer

@implementer(ILoggingContext)
class InfluxDatabaseService(ApplicationSession):
    """An application component for logging telemetry data to InfluxDB databases"""

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
        self.influx = InfluxDBClient('192.168.59.103', 8086, 'root', 'root', 'kotori')
        self.influx.create_database('kotori')

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
            if self.influx:

                data = [
                    {
                        "name" : "telemetry",
                        "columns" : ["mma_x", "mma_y", "temp"],
                        "points" : [
                            [mma_x, mma_y, temp]
                        ]
                    }
                ]

                self.influx.write_points(data)

        except ValueError:
            print('Could not decode data: {}'.format(data))


def boot_influx_database(websocket_uri, debug=False):

    print 'INFO: Starting influx database service, connecting to broker', websocket_uri

    runner = ApplicationRunner(websocket_uri, "kotori-realm", debug=False, debug_wamp=False, debug_app=False)
    runner.run(InfluxDatabaseService, start_reactor=False)
