# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.sql.schema import MetaData, Column, Table
from sqlalchemy.sql.sqltypes import Integer, String, Numeric
from alchimia.strategy import TWISTED_STRATEGY
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

class SqlDatabaseService(ApplicationSession):
    """An application component for logging telemetry data to sql databases"""

    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        self.count = 0
        self.engine = None

        metadata = MetaData()
        self.telemetry = Table("telemetry", metadata,
            Column("id", Integer(), primary_key=True),
            Column("mma_x", Integer()),
            Column("mma_y", Integer()),
            Column("temp", Numeric()),
	    Column("lat", Numeric()),
	    Column("lng", Numeric()),
        )

    @inlineCallbacks
    def onJoin(self, details):
        print("Realm joined (WAMP session started).")

        # subscribe to telemetry data channel
        self.subscribe(self.receive, u'de.elmyra.kotori.telemetry.data')

        self.startDatabase()

        #self.leave()

    @inlineCallbacks
    def startDatabase(self):
        self.engine = create_engine(

            # sqlite in-memory
            #"sqlite://", reactor=reactor, strategy=TWISTED_STRATEGY

            # sqlite on filesystem
            "sqlite:////tmp/kotori.sqlite", reactor=reactor, strategy=TWISTED_STRATEGY

            # mysql... todo
        )

        # Create the table
        yield self.engine.execute(CreateTable(self.telemetry))
        #yield self.engine

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
        mma_x = int(payload[0])
        mma_y = int(payload[1])
        temp = float(payload[2])
        try:
            lat = float(payload[3])
            lng = float(payload[4])
        except:
            lat = 0
            lng = 0

        # store data to database
        if self.engine:
            yield self.engine.execute(self.telemetry.insert().values(mma_x = mma_x, mma_y = mma_y, temp = temp, lat = lat, lng = lng))


def boot_sql_database(websocket_uri, debug=False):

    print 'INFO: Starting sql database service, connecting to broker', websocket_uri

    runner = ApplicationRunner(websocket_uri, "kotori-realm", debug=False, debug_wamp=False, debug_app=False)
    runner.run(SqlDatabaseService, start_reactor=False)
