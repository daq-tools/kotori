# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from influxdb.influxdb08 import InfluxDBClient
from influxdb.influxdb08.client import InfluxDBClientError
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

    #@inlineCallbacks
    def onJoin(self, details):
        print("Realm joined (WAMP session started).")

        # subscribe to telemetry data channel
        self.subscribe(self.receive, u'de.elmyra.kotori.telemetry.data')

        self.startDatabase()

        #self.leave()

    #@inlineCallbacks
    def startDatabase(self):

        # production: InfluxDB on localhost
        #database_name = 'kotori_2'
        #self.influx = InfluxDBClient('127.0.0.1', 8086, 'root', 'BCqIJvslOnJ9S4', database_name)

        # development: InfluxDB on Docker host
        database_name = 'kotori-dev'
        self.influx = InfluxDBClient('192.168.59.103', 8086, 'root', 'root', database_name)

        try:
            self.influx.create_database(database_name)

        except InfluxDBClientError as ex:
            # ignore "409: database kotori-dev exists"
            if ex.code == 409:
                pass
            else:
                raise

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
        try:
            MSG_ID          = int(payload[0])
            V_FC            = float(payload[1]) * 0.001
            V_CAP           = float(payload[2]) * 0.001
            A_ENG           = float(payload[3]) * 0.001
            A_CAP           = float(payload[4]) * 0.001
            T_O2_In         = float(payload[5]) * 0.1
            T_O2_Out        = float(payload[6]) * 0.1
            T_FC_H2O_Out    = float(payload[7]) * 0.1
            Water_In        = float(payload[8])
            Water_Out       = float(payload[9])
            Master_SW       = bool(payload[10])
            CAP_Down_SW     = bool(payload[11])
            Drive_SW        = bool(payload[12])
            FC_state        = bool(payload[13])
            Mosfet_state    = bool(payload[14])
            Safety_state    = bool(payload[15])
            Air_Pump_load   = float(payload[16]) * 0.1
            Mosfet_load     = float(payload[17]) * 0.1
            Water_Pump_load = float(payload[18]) * 0.1
            Fan_load        = float(payload[19]) * 0.1
            Acc_X           = float(payload[20]) * 0.001
            Acc_Y           = float(payload[21]) * 0.001
            Acc_Z           = float(payload[22]) * 0.001
            H2_flow         = float(payload[23]) * 0.001
            GPS_X           = float(payload[24]) * 0.01
            GPS_Y           = float(payload[25]) * 0.01
            GPS_Z           = float(payload[26]) * 0.01
            GPS_Speed       = float(payload[27]) * 0.01
            V_Safety        = float(payload[28]) * 0.001
            H2_Level        = int(payload[29])
            O2_calc         = float(payload[30]) * 0.01
            lat             = float(payload[31])
            lng             = float(payload[32])
            P_In            = A_CAP * V_FC
            P_Out           = A_ENG * V_CAP




           # store data to database
            if self.influx:

               data = [
                   {
                       "name" : "telemetry",
                       "columns" : ["MSG_ID", "V_FC", "V_CAP", "A_ENG", "A_CAP", "T_O2_In", "T_O2_Out", "T_FC_H2O_Out", "Water_In", "Water_Out", "Master_SW", "CAP_Down_SW", "Drive_SW", "FC_state", "Mosfet_state", "Safety_state", "Air_Pump_load", "Mosfet_load", "Water_Pump_load", "Fan_load", "Acc_X", "Acc_Y", "Acc_Z", "H2_flow", "GPS_X", "GPS_Y", "GPS_Z", "GPS_Speed", "V_Safety", "H2_Level", "O2_calc", "lat", "lng", "P_In", "P_Out"],
                       "points" : [
                           [MSG_ID, V_FC, V_CAP, A_ENG, A_CAP, T_O2_In, T_O2_Out, T_FC_H2O_Out, Water_In, Water_Out, Master_SW, CAP_Down_SW, Drive_SW, FC_state, Mosfet_state, Safety_state, Air_Pump_load, Mosfet_load, Water_Pump_load, Fan_load, Acc_X, Acc_Y, Acc_Z, H2_flow, GPS_X, GPS_Y, GPS_Z, GPS_Speed, V_Safety, H2_Level, O2_calc, lat, lng, P_In, P_Out]
                       ]
                   }
               ]
               self.influx.write_points(data)
               print "Saved event to InfluxDB"


#            mma_x = int(payload[0])
#            mma_y = int(payload[1])
#            temp = float(payload[2])
#
#            # store data to database
#            if self.influx:
#
#                data = [
#                    {
#                        "name" : "telemetry",
#                        "columns" : ["mma_x", "mma_y", "temp"],
#                        "points" : [
#                            [mma_x, mma_y, temp]
#                        ]
#                    }
#                ]
#


        except ValueError:
            print('Could not decode data: {}'.format(data))


def h2m_boot_influx_database(websocket_uri, debug=False, trace=False):

    print 'INFO: Starting influx database service, connecting to broker', websocket_uri

    runner = ApplicationRunner(websocket_uri, u'kotori-realm', debug=trace, debug_wamp=debug, debug_app=debug)
    runner.run(InfluxDatabaseService, start_reactor=False)
