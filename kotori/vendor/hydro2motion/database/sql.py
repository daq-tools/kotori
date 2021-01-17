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
            Column("MSG_ID", Integer()),
            Column("V_FC", Integer()),
            Column("V_CAP", Integer()),
            Column("A_ENG", Integer()),
            Column("A_CAP", Integer()),
            Column("T_O2_In", Integer()),
            Column("T_O2_Out", Integer()),
            Column("T_FC_H2O_Out", Integer()),
            Column("Water_In", Integer()),
            Column("Water_Out", Integer()),
            Column("Master_SW", Integer()),
            Column("CAP_Down_SW", Integer()),
            Column("Drive_SW", Integer()),
            Column("FC_state", Integer()),
            Column("Mosfet_state", Integer()),
            Column("Safety_state", Integer()),
            Column("Air_Pump_load", Numeric()),
            Column("Mosfet_load", Integer()),
            Column("Water_Pump_load", Integer()),
            Column("Fan_load", Integer()),
            Column("Acc_X", Integer()),
            Column("Acc_Y", Integer()),
            Column("Acc_Z", Integer()),
            Column("AUX", Numeric()),
            Column("GPS_X", Integer()),
            Column("GPS_Y", Integer()),
            Column("GPS_Z", Integer()),
            Column("GPS_Speed", Integer()),
            Column("V_Safety", Integer()),
            Column("H2_Level", Integer()),
            Column("O2_calc", Numeric()),
            Column("lat", Numeric()),
            Column("lng", Numeric()),
            )


#        metadata = MetaData()
#        self.telemetry = Table("telemetry", metadata,
#            Column("id", Integer(), primary_key=True),
#            Column("mma_x", Integer()),
#            Column("mma_y", Integer()),
#            Column("temp", Numeric()),
#	    Column("lat", Numeric()),
#	    Column("lng", Numeric()),
#        )

    #@inlineCallbacks
    def onJoin(self, details):
        print("Realm joined (WAMP session started).")

        # subscribe to telemetry data channel
        self.subscribe(self.receive, u'de.elmyra.kotori.telemetry.data')

        self.startDatabase()

        #self.leave()

    #@inlineCallbacks
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
        ApplicationSession.onLeave(self, details)

    def onDisconnect(self):
        print("Transport disconnected.")
        #reactor.stop()

    #@inlineCallbacks
    def receive(self, data):
        #print "RECEIVE:", data

        # decode wire data
        payload = data.split(';')
        MSG_ID          = int(payload[0])
        V_FC            = int(payload[1])
        V_CAP           = int(payload[2])
        A_ENG           = int(payload[3])
        A_CAP           = int(payload[4])
        T_O2_In         = int(payload[5])
        T_O2_Out        = int(payload[6])
        T_FC_H2O_Out    = int(payload[7])
        Water_In        = int(payload[8])
        Water_Out       = int(payload[9])
        Master_SW       = int(payload[10])
        CAP_Down_SW     = int(payload[11])
        Drive_SW        = int(payload[12])
        FC_state        = int(payload[13])
        Mosfet_state    = int(payload[14])
        Safety_state    = int(payload[15])
        Air_Pump_load   = float(payload[16])
        Mosfet_load     = int(payload[17])
        Water_Pump_load = int(payload[18])
        Fan_load        = int(payload[19])
        Acc_X           = int(payload[20])
        Acc_Y           = int(payload[21])
        Acc_Z           = int(payload[22])
        AUX             = float(payload[23])
        GPS_X           = int(payload[24])
        GPS_Y           = int(payload[25])
        GPS_Z           = int(payload[26])
        GPS_Speed       = int(payload[27])
        V_Safety        = int(payload[28])
        H2_Level        = int(payload[29])
        O2_calc         = float(payload[30])
        lat             = float(payload[31])
        lng             = float(payload[32])




#        mma_x = int(payload[0])
#        mma_y = int(payload[1])
#        temp = float(payload[2])
#        try:
#            lat = float(payload[3])
#            lng = float(payload[4])
#        except:
#            lat = 0
#            lng = 0

        # store data to database
        if self.engine:
            yield self.engine.execute(self.telemetry.insert().values(MSG_ID = MSG_ID, V_FC = V_FC, V_CAP = V_CAP, A_ENG = A_ENG, A_CAP = A_CAP, T_O2_In = T_O2_In, T_O2_Out = T_O2_Out, T_FC_H2O_Out = T_FC_H2O_Out, Water_In = Water_In, Water_Out = Water_Out, Master_SW = Master_SW, CAP_Down_SW = CAP_Down_SW, Drive_SW = Drive_SW, FC_state = FC_state, Mosfet_state = Mosfet_state, Safety_state = Safety_state, Air_Pump_load = Air_Pump_load, Mosfet_load = Mosfet_load, Water_Pump_load = Water_Pump_load, Fan_load = Fan_load, Acc_X = Acc_X, Acc_Y = Acc_Y, Acc_Z = Acc_Z, AUX = AUX, GPS_X = GPS_X, GPS_Y = GPS_Y, GPS_Z = GPS_Z, GPS_Speed = GPS_Speed, V_Safety = V_Safety, H2_Level = H2_Level, lat = lat, lng = lng))


def boot_sql_database(websocket_uri, debug=False, trace=False):

    print('INFO: Starting sql database service, connecting to broker', websocket_uri)

    runner = ApplicationRunner(websocket_uri, u'kotori-realm', debug=trace, debug_wamp=debug, debug_app=debug)
    runner.run(SqlDatabaseService, start_reactor=False)
