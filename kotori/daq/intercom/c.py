# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import logging
from cornice.util import to_list
from collections import OrderedDict
from ctypes import c_uint8, c_uint16, c_uint32, c_int8, c_int16, c_int32
from pyclibrary import CLibrary, auto_init
from pyclibrary.utils import add_header_locations, add_library_locations
from pyclibrary.c_parser import Type, integer
from kotori.daq.intercom.pyclibrary_ext.c_parser import CParserEnhanced
from kotori.daq.intercom.pyclibrary_ext.backend_ctypes import monkeypatch_pyclibrary_ctypes_struct

logger = logging.getLogger(__name__)


class LibraryAdapter(object):

    def __init__(self, header_files, library_file, include_path=None, library_path=None, cache_path=None):
        self.header_files = to_list(header_files)
        self.library_file = library_file
        self.include_path = include_path or os.curdir
        self.library_path = library_path or os.curdir
        self.cache_path = cache_path or './var'

        cache_key = u'_'.join(self.header_files) + '.pyclibrary'
        self.cache_file = os.path.join(self.cache_path, cache_key)

        self.setup()
        self.parse()
        self.load()

    def setup(self):

        # counter "ValueError: number of bits invalid for bit field"
        monkeypatch_pyclibrary_ctypes_struct()

        # register header- and library paths
        # https://pyclibrary.readthedocs.org/en/latest/get_started/configuration.html#specifying-headers-and-libraries-locations
        #curr_dir = os.path.dirname(__file__)
        curr_dir = os.curdir
        # TODO: this probably acts on a global basis; think about it
        add_header_locations([self.include_path])
        add_library_locations([self.library_path])

        # define extra types suitable for embedded use
        types = {
            'uint8_t': c_uint8,
            'uint16_t': c_uint16,
            'uint32_t': c_uint32,
            'int8_t': c_int8,
            'int16_t': c_int16,
            'int32_t': c_int32,
            }
        auto_init(extra_types=types)

    def parse(self):
        # use an improved CParser which can grok/skip more constructor flavours
        self.parser = CParserEnhanced(self.header_files, cache=self.cache_file)

    def load(self):
        self.clib = CLibrary(self.library_file, self.parser, prefix='Lib_', lock_calls=False, convention='cdll', backend='ctypes')

    def struct_names(self):
        return self.parser.defs['structs'].keys()


class StructAdapter(object):

    def __init__(self, name, library):
        self.name = name
        self.library = library
        self.parser = self.library.parser
        self.clib = self.library.clib

    def ast(self):
        return self.parser.defs['structs'][self.name]

    def obj(self):
        return self.clib('structs', self.name)

    def create(self, **attributes):
        return self.obj()(**attributes)


class StructRegistry(object):

    def __init__(self, library):
        self.library = library

        # dictionary of structs, by name
        self.structs = {}

        self.build()

    def build(self):
        for name in self.library.struct_names():
            logger.info('Rolling in struct "{}"'.format(name))
            self.register_adapter(name)

    def register_adapter(self, name):
                # store adapter object by name
        adapter = StructAdapter(name, self.library)
        self.structs[name] = adapter
        return adapter

    def get(self, name):
        return self.structs[name]

    def get_by_id(self, struct_id):
        return self.structs_by_id[struct_id]

    def create(self, name, **attributes):
        return self.get(name).create(**attributes)

    @staticmethod
    def to_dict(struct):
        fieldnames = [field[0] for field in struct._fields_]
        d = OrderedDict()
        for fieldname in fieldnames:
            d[fieldname] = getattr(struct, fieldname)
        return d


class StructRegistryByID(StructRegistry):

    # TODO: Make generic like ``sr = StructRegistryByID(library, indexes=['ID'])``

    def __init__(self, library, indexes=None):
        # dictionary of structs, by id
        self.structs_by_id = {}
        StructRegistry.__init__(self, library)

    def register_adapter(self, name):

        adapter = StructRegistry.register_adapter(self, name)

        # store adapter object by id
        struct_id = adapter.create().ID
        if self.structs_by_id.has_key(struct_id):
            o_a = self.structs_by_id[struct_id]
            name_owner = o_a.name
            logger.warning('Struct "{}" has ID "{}", but this is already owned by "{}". '\
                           'Please check if struct provides reasonable default values for attribute "ID".'.format(name, struct_id, name_owner))
        else:
            logger.info('Struct "{}" now owns ID "{}".'.format(name, struct_id))
            self.structs_by_id[struct_id] = adapter
