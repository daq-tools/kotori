# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from binascii import hexlify
from cornice.util import to_list
from twisted.logger import Logger
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.defer import inlineCallbacks


class UdpBusForwarder(DatagramProtocol):
    # https://twistedmatrix.com/documents/15.0.0/core/howto/udp.html

    def __init__(self, bus, topic, transform, logger):
        self.bus = bus
        self.topic = topic
        self.transform = to_list(transform)
        self.log = logger or Logger()

        # TODO sanity checks

    @inlineCallbacks
    def datagramReceived(self, data, addr):

        (host, port) = addr

        self.log.debug(u"Received via UDP from {host}:{port}: {data}", host=host, port=port, data=hexlify(data))

        # ECHO
        #self.transport.write(data, (host, port))

        # apply transformation steps
        data_out = data
        for transform in self.transform:
            data_out = transform(data_out)

        # forward
        self.log.debug(u"Publishing to topic '{topic}' with realm '{realm}': {data}",
            topic=self.topic, realm=self.bus._realm, data=data_out)

        yield self.bus.publish(self.topic, data_out)
