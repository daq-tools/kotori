# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import logging
from collections import OrderedDict

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

    def pprint(self, struct, data=None, format='tabulate-plain'):
        # pretty-print struct content
        # TODO: maybe refactor to struct._pprint_
        self.struct_registry.pprint(struct, data=data, format=format)

    def to_dict(self, struct):
        # convert struct content to json
        # TODO: maybe refactor to struct._json_
        return self.struct_registry.to_dict(struct)

    def transform(self, struct):
        """
        apply transformation rules to struct
        """

        # convert struct to OrderedDict
        data = self.struct_registry.to_dict(struct)

        # look up proper StructAdapter object
        struct_schema = self.struct_registry.get_by_id(struct.ID)

        # get annotations object
        annotations = struct_schema.annotations

        # prepare variables suitable for expression evaluation
        # TODO: make check against "null bytes" more generic
        variables = dict(data)
        del variables['ck']     # otherwise: "TypeError: expected string without null bytes" from SymPy

        # apply transformation rules, keep item order
        data_new = OrderedDict()
        for key, value in data.items():

            # get transformation rule
            rule = annotations.get_struct_rule(struct_schema.name, key)
            if rule:

                # apply expression
                if 'expression_sympy' in rule:
                    expr = rule['expression_sympy']

                    # always gives (SymPy) Floats or Zero, never Integer :-(
                    value = expr.subs(variables).evalf()

                    # convert to Python-native data types
                    # TODO: check if SymPy provides a generic builtin for that
                    if value.is_zero:
                        value = 0.0
                    elif value.is_Float:
                        value = float(value)

                # apply field renaming
                if 'name' in rule:
                    key = rule['name']

            data_new[key] = value

        return data_new

