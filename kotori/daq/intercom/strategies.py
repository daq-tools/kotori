# -*- coding: utf-8 -*-
# (c) 2015-2018 Andreas Motl, <andreas@getkotori.org>
import re
from kotori.util.common import SmartBunch


class WanBusStrategy(object):

    def __init__(self, *args, **kwargs):
        pass

    def topic_to_topology(self, topic):
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
              the collaborative ether, though.
              So the best thing would be to give kind of nicknames to your
              sites which don't identify their location.

            - "1" is your node identifier. Choose anything you like. This usually
              gets transmitted from an embedded device node. Remember one device node
              might have multiple sensors attached, which is beyond the scope of the
              collection platform: We just accept bunches of named measurement values,
              no matter which sensors they might originate from.
              In other words: We don't need nor favor numeric sensor identifiers,
              let's give them names!
        """

        # regular expression pattern for decoding MQTT topic address segments
        pattern = r'^(?P<realm>.+?)/(?P<network>.+?)/(?P<gateway>.+?)/(?P<node>.+?)(?:/(?P<slot>.+?))?$'

        # decode the topic
        p = re.compile(pattern)
        m = p.match(topic)
        if m:
            address = SmartBunch(m.groupdict())
        else:
            address = {}

        return address


    @classmethod
    def topology_to_storage(self, topology):
        """
        Encode topology segment identifiers to database address.

        A database server usually has the concept of multiple databases,
        each with multiple tables. With other databases than RDBMS,
        they might be named differently, but the concept in general
        is the same.

        When mapping the topology quadruple (realm, network, gateway, node) in the form of:

            - realm + network = database name
            - gateway + node  = table name

        We have a perfect fit for computing the slot where to store the measurements.

        """

        # Todo: Investigate using tags additionally to / instead of database.measurement
        # Todo: Move specific stuff about WeeWX or Tasmota to some device-specific knowledgebase.

        # data:     Regular endpoint
        # loop:     WeeWX
        # SENSOR:   Sonoff-Tasmota
        if topology.slot.startswith('data') or topology.slot.startswith('loop') \
                or topology.slot.endswith('SENSOR') or topology.slot.endswith('STATE'):
            suffix = 'sensors'

        elif topology.slot.startswith('event'):
            suffix = 'events'

        else:
            suffix = 'unknown'

        # Use topology information as blueprint for storage address
        storage = SmartBunch(topology)

        # Format and sanitize all input parameters used for database addressing
        sanitize = self.sanitize_db_identifier
        storage.label       = sanitize('{}-{}'.format(storage.gateway, storage.node))
        storage.database    = sanitize('{}_{}'.format(storage.realm, storage.network))
        storage.measurement = sanitize('{}_{}_{}'.format(storage.gateway, storage.node, suffix))
        storage.measurement_events = sanitize('{}_{}_{}'.format(storage.gateway, storage.node, 'events'))

        return storage

    @classmethod
    def topology_to_label(cls, topology):
        return '{}-{}-{}-{}'.format(topology.realm, topology.network, topology.gateway, topology.node)

    @staticmethod
    def sanitize_db_identifier(value):
        """
        Different databases accept different special
        characters as database- or table names.

        Better safe than sorry, let's strip them all.
        """
        value = value.replace('/', '_').replace('.', '_').replace('-', '_').lower()
        return value
