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

    #@inlineCallbacks
    def onJoin(self, details):
        print("Realm joined (WAMP session started).")

        # subscribe to telemetry data channel
        self.subscribe(self.receive, u'de.elmyra.kotori.telemetry.data')

        self.startDatabase()

        #self.leave()

    #@inlineCallbacks
    def startDatabase(self):
        #self.mongo = yield txmongo.MongoConnection(host='127.0.0.0', port=27017)
        self.mongo = yield txmongo.MongoConnection()

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
            V_FC            = int(payload[1])
            V_CAP           = int(payload[2])
            A_ENG           = int(payload[3])
            A_CAP           = int(payload[4])
            T_O2_In         = int(payload[5])
            T_O2_Out        = int(payload[6])
            T_FC_H2O_Out    = int(payload[7])
            Water_In        = int(payload[8])
            Water_Out       = int(payload[9])
            Master_SW       = bool(payload[10])
            CAP_Down_SW     = bool(payload[11])
            Drive_SW        = bool(payload[12])
            FC_state        = bool(payload[13])
            Mosfet_state    = bool(payload[14])
            Safety_state    = bool(payload[15])
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

            # store data to database
            if self.mongo:
                telemetry = self.mongo.kotori.telemetry
                yield telemetry.insert(dict(MSG_ID = MSG_ID, V_FC = V_FC, V_CAP = V_CAP, A_ENG = A_ENG, A_CAP = A_CAP, T_O2_In = T_O2_In, T_O2_Out = T_O2_Out, T_FC_H2O_Out = T_FC_H2O_Out, Water_In = Water_In, Water_Out = Water_Out, Master_SW = Master_SW, CAP_Down_SW = CAP_Down_SW, Drive_SW = Drive_SW, FC_state = FC_state, Mosfet_state = Mosfet_state, Safety_state = Safety_state, Air_Pump_load = Air_Pump_load, Mosfet_load = Mosfet_load, Water_Pump_load = Water_Pump_load, Fan_load = Fan_load, Acc_X = Acc_X, Acc_Y = Acc_Y, Acc_Z = Acc_Z, AUX = AUX, GPS_X = GPS_X, GPS_Y = GPS_Y, GPS_Z = GPS_Z, GPS_Speed = GPS_Speed, V_Safety = V_Safety, H2_Level = H2_Level, O2_calc = O2_calc, lat = lat, lng = lng))

        except ValueError:
            print('Could not decode data: {}'.format(data))


def boot_mongo_database(websocket_uri, debug=False, trace=False):

    print('INFO: Starting mongo database service, connecting to broker', websocket_uri)

    runner = ApplicationRunner(websocket_uri, u'kotori-realm', debug=trace, debug_wamp=debug, debug_app=debug)
    runner.run(MongoDatabaseService, start_reactor=False)
