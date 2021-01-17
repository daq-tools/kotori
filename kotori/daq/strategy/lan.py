# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl, <andreas@getkotori.org>
import re

from kotori.daq.strategy import StrategyBase
from kotori.util.common import SmartBunch


class LanStrategy(StrategyBase):

    # Regular expression pattern for decoding MQTT topic address segments.
    pattern = r'^(?P<realm>.+?)/(?P<node>.+?)(?:/(?P<slot>.+?))?$'
    matcher = re.compile(pattern)

    def topic_to_topology(self, topic):
        """
        Decode MQTT topic segments implementing the »basic strategy«.

        The topology hierarchy is directly specified by the MQTT topic and is
        made up of a two path segments::

            realm / node

        The topology identifiers are specified as:

            - "realm" is the designated root realm. You should prefix the topic name
              with this label when opting in for all features of the telemetry platform.
              For other purposes, feel free to publish to any MQTT topic you like.

            - "node" is the node identifier. Choose anything you like. This usually
              gets transmitted from an embedded device node.
        """

        # decode the topic
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

        The topology information (realm, node) will
        get mapped to the database name and measurement name to
        compute the storage location for measurements.

            - realm + node     = database name
            - sensors | events = table name

        """

        # Derive database table suffix from message type.
        table_suffix = self.get_table_suffix(topology, message_type)

        # Use topology information as blueprint for storage address.
        storage = SmartBunch(topology)

        # Format and sanitize all input parameters used for database addressing.
        # Todo: Investigate using tags additionally to / instead of only "storage.measurement".
        sanitize = self.sanitize_db_identifier
        storage.label       = sanitize('{}'.format(storage.node))
        storage.database    = sanitize('{}_{}'.format(storage.realm, storage.node))
        storage.measurement = sanitize('{}'.format(table_suffix))
        storage.measurement_events = sanitize('{}'.format('events'))

        return storage

    @classmethod
    def topology_to_label(cls, topology):
        return '{}-{}'.format(topology.realm, topology.node)
