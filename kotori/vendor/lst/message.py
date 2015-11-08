# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import logging
from binascii import unhexlify
from tabulate import tabulate

logger = logging.getLogger(__name__)

class BinaryMessageAdapter(object):

    def __init__(self, struct_registry):
        self.struct_registry = struct_registry

    def decode(self, payload):

        # decode data payload from 8-bit clean hex format, e.g. ``05022a0021``
        logger.debug('Decoding hex payload "{}"'.format(payload))
        payload = unhexlify(payload)

        # decode struct ID from binary data, it's always at the second byte
        message_id = ord(payload[1])
        logger.debug('Message struct ID is "{}"'.format(message_id))

        # look up proper StructAdapter object
        struct_schema = self.struct_registry.get_by_id(message_id)

        # create instance of struct
        struct = struct_schema.create()

        # load binary message payload into struct
        struct._load_(payload)

        return struct

    def pprint(self, struct, format='tabulate-plain'):
        # pretty-print struct content
        self.struct_registry.pprint(struct, format=format)

