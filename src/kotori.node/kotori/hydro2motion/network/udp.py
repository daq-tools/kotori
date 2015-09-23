# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import DatagramProtocol
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession, ApplicationSessionFactory
from kotori.hydro2motion.util.geo import turn_xyz_into_llh

# https://twistedmatrix.com/documents/15.0.0/core/howto/udp.html

app_session = None

class UdpPublisher(ApplicationSession):
    """
    Simple message publishing with Autobahn WebSockets.

    derived from:
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/basic/pubsub/basic/frontend.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/session/fromoutside/client.py
    """

    #@inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        global app_session
        app_session = self


    def onDisconnect(self):
        print("disconnected")
        #reactor.stop()


def run_wamp_client():
    #log.startLogging(sys.stdout)

    # connect to crossbar router/broker
    runner = ApplicationRunner(u'ws://localhost:9000/ws', u'kotori-realm')
    #runner = ApplicationRunner("ws://master.example.com:9000/ws", "kotori-realm")

    runner.run(UdpPublisher, start_reactor=False)



class UdpAdapter(DatagramProtocol):

    @inlineCallbacks
    def datagramReceived(self, data, (host, port)):
        print "Received via UDP from %s:%d: %r " % (host, port, data)

        try:
         payload = data.split(';')
         GPS_X           = int(payload[24])
         GPS_Y           = int(payload[25])
         GPS_Z           = int(payload[26])

         x = GPS_X / 100.0
         y = GPS_Y / 100.0
         z = GPS_Z / 100.0


         llh = turn_xyz_into_llh(x, y, z, "wgs84")
         lat = llh[0]
         lng = llh[1]

         seq = (data, str(lat), str(lng))

         jdata = ";".join(seq)

#         lat = float(lat_i) / 100.0
#         lng = float(lng_i) / 100.0

#         data.append(';')
#         data.append(lat)
#         data.append(';')
#         data.append(str(lng))

        except ValueError:
            print('Could not decode data: {}'.format(jdata))


        # ECHO
        #self.transport.write(data, (host, port))

        # forward
        yield app_session.publish(u'de.elmyra.kotori.telemetry.data', jdata)



def h2m_boot_udp_adapter(udp_port, debug=False):

    run_wamp_client()

    print 'INFO: Starting udp adapter on port', udp_port
    reactor.listenUDP(udp_port, UdpAdapter())
