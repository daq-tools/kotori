# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl, <andreas@getkotori.org>
import re

from kotori.daq.strategy import StrategyBase
from kotori.util.common import SmartBunch


class WanBusStrategy(StrategyBase):

    # Regular expression pattern for decoding MQTT topic address segments.
    pattern = r'^(?P<realm>.+?)/(?P<network>.+?)/(?P<gateway>.+?)/(?P<node>.+?)(?:/(?P<slot>.+?))?$'
    matcher = re.compile(pattern)

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
              the collaborative ether, though. You might want to assign nicknames
              to your sites to not identify their location.

            - "node" is the node identifier. Choose anything you like. This usually
              gets transmitted from an embedded device node.
        """

        # Decode the topic.
        m = self.matcher.match(topic)
        if m:
            address = SmartBunch(m.groupdict())
        else:
            address = {}

        return address

    @classmethod
    def topology_to_storage(self, topology, message_type=None):
        """
        Encode topology segment identifiers to database address.

        A database server usually has the concept of multiple databases,
        each with multiple tables. With other databases than RDBMS,
        they might be named differently, but the concept in general
        is the same.

        The topology quadruple (realm, network, gateway, node) will
        get mapped to the database name and measurement name to
        compute the storage location for measurements.

            - realm + network = database name
            - gateway + node  = table name

        """

        # Derive database table suffix from message type.
        table_suffix = self.get_table_suffix(topology, message_type)

        # Use topology information as blueprint for storage address.
        storage = SmartBunch(topology)

        # Format and sanitize all input parameters used for database addressing.
        # Todo: Investigate using tags additionally to / instead of only "storage.measurement".
        sanitize = self.sanitize_db_identifier
        storage.label       = sanitize('{}-{}'.format(storage.gateway, storage.node))
        storage.database    = sanitize('{}_{}'.format(storage.realm, storage.network))
        storage.measurement = sanitize('{}_{}_{}'.format(storage.gateway, storage.node, table_suffix))
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
