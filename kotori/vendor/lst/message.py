# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import logging

logger = logging.getLogger(__name__)

class BinaryMessageAdapter(object):

    def __init__(self, struct_registry):
        self.struct_registry = struct_registry

    def decode(self, payload):

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
        # TODO: maybe refactor to struct._pprint_
        self.struct_registry.pprint(struct, format=format)

    def to_dict(self, struct):
        # convert struct content to json
        # TODO: maybe refactor to struct._json_
        return self.struct_registry.to_dict(struct)
