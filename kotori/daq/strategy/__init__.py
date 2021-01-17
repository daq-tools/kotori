# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl, <andreas@getkotori.org>
from kotori.daq.decoder import MessageType


class StrategyBase:

    @staticmethod
    def sanitize_db_identifier(value):
        """
        Different databases accept different special
        characters as database- or table names.

        Better safe than sorry, let's strip them all.
        """
        value = value.replace('/', '_').replace('.', '_').replace('-', '_').lower()
        return value

    @staticmethod
    def get_table_suffix(topology, message_type=None):
        """
        Derive database table suffix from message type.
        """
        if message_type in (MessageType.DATA_CONTAINER, MessageType.DATA_DISCRETE) or topology.slot.startswith('data'):
            suffix = 'sensors'
        elif message_type == MessageType.EVENT or topology.slot.startswith('event'):
            suffix = 'events'
        else:
            suffix = 'unknown'
        return suffix
