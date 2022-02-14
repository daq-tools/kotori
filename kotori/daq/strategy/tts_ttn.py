# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl, <andreas@getkotori.org>
import re

from munch import Munch

from kotori.daq.strategy.wan import WanBusStrategy
from kotori.util.common import SmartBunch


class TheThingsWanBusStrategy(WanBusStrategy):

    # Regular expression pattern for decoding MQTT topic address segments.
    #pattern = r'^(?P<realm>.+?)/ttn/(?P<device_id>.+?)(?:/(?P<slot>.+?))?$'
    #matcher = re.compile(pattern)

    @classmethod
    def topic_to_topology(cls, topic):
        """
        Decode MQTT topic segments implementing the »quadruple hierarchy strategy«.

        The topology hierarchy is directly specified by the MQTT topic and is
        made up of a minimum of four identifiers describing the core structure::

            realm / network / gateway / node

        The topology identifiers are specified as:

            - "realm" is the designated root realm. You should prefix the topic name
              with this label when opting in for all features of the telemetry platform.
              For other purposes, feel free to publish to any MQTT topic you like.

            - "network" is your personal realm. Choose anything you like or use an
              `Online GUID Generator <https://www.guidgenerator.com/>`_ to gain
              maximum uniqueness.

            - "gateway" is your gateway identifier. Choose anything you like.
              This does not have to be very unique, so you might use labels
              having the names of sites. While you are the owner of this
              namespace hierarchy, remember these labels might be visible on
              the collaborative ether, though. You might want to assign nicknames
              to your sites to not identify their location.

            - "node" is the node identifier. Choose anything you like. This usually
              gets transmitted from an embedded device node.
        """

        print("########## TOPIC:", topic)

        # Munch({'realm': 'mqttkit-1', 'device_id': 'itest-foo-bar', 'slot': 'uplinks'})
        assert isinstance(topic, Munch)
        assert topic.realm
        assert topic.device_id
        assert topic.slot

        # {'realm': 'mqttkit-1', 'network': 'itest', 'gateway': 'foo', 'node': 'bar', 'slot': 'data.json'}
        address = SmartBunch(
            realm=topic.realm,

        )


        # Decode the topic.
        m = cls.matcher.match(topic)
        if m:
            address = SmartBunch(m.groupdict())
        else:
            address = {}

        return address
