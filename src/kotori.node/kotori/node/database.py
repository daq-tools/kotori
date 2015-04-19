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

class DatabaseService(ApplicationSession):

    """
    An application component using the time service
    during 3 subsequent WAMP sessions, while the
    underlying transport continues to exist.
    """

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
        )


    @inlineCallbacks
    def onJoin(self, details):
        print("Realm joined (WAMP session started).")

        self.subscribe(self.receive, u'de.elmyra.kotori.telemetry.data')

        try:
            now = yield self.call('com.timeservice.now')
        except Exception as e:
            print("Error: {}".format(e))
        else:
            print("Current time from time service: {}".format(now))


        yield self.publish(u'de.elmyra.kotori.telemetry.data', 'hello world')

        #self.leave()
        self.startDatabase()

    @inlineCallbacks
    def startDatabase(self):
        self.engine = create_engine(
            #"sqlite://", reactor=reactor, strategy=TWISTED_STRATEGY
            "sqlite:////tmp/kotori.sqlite", reactor=reactor, strategy=TWISTED_STRATEGY
        )

        # Create the table
        yield self.engine.execute(CreateTable(self.telemetry))
        yield self.engine

    def onLeave(self, details):
        print("Realm left (WAMP session ended).")

    def onDisconnect(self):
        print("Transport disconnected.")
        #reactor.stop()

    @inlineCallbacks
    def receive(self, data):
        #print "RECEIVE:", data

        # decode data
        payload = data.split(';')
        mma_x = int(payload[0])
        mma_y = int(payload[1])
        temp = float(payload[2])

        #print self.engine
        if self.engine:
            yield self.engine.execute(self.telemetry.insert().values(mma_x = mma_x, mma_y = mma_y, temp = temp))

    def dump_event(self, *args, **kwargs):
        print "dump_event:", {'args': args, 'kwargs': kwargs}


def boot_database(websocket_uri, debug=False):

    print 'INFO: Starting database service, connecting to', websocket_uri

    # connect to master service
    """
    global node_manager
    node_manager = NodeManager(websocket_uri, debug=debug)
    reactor.callLater(0, node_manager.master_connect)
    """

    runner = ApplicationRunner(websocket_uri, "kotori-realm", debug=False, debug_wamp=False, debug_app=False)
    runner.run(DatabaseService, start_reactor=False)

    #app = Application()
    #app.run(url=websocket_uri, realm='kotori-realm', debug=True, debug_wamp=True, debug_app=True, start_reactor=False)
