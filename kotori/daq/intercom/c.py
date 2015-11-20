# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
from collections import OrderedDict
from cornice.util import to_list
from pprint import pprint
from binascii import hexlify
from tabulate import tabulate
from appdirs import user_cache_dir
from pyclibrary.c_parser import CParser
from ctypes import c_uint8, c_uint16, c_uint32, c_int8, c_int16, c_int32
from pyclibrary import CLibrary, auto_init
from pyclibrary.utils import add_header_locations, add_library_locations
from twisted.logger import Logger
from kotori.daq.intercom.pyclibrary_ext.c_parser import CParserEnhanced
from kotori.daq.intercom.pyclibrary_ext.backend_ctypes import monkeypatch_pyclibrary_ctypes_struct
from kotori.util import slm

#logger = logging.getLogger(__name__)
logger = Logger()

class LibraryAdapter(object):

    def __init__(self, header_files, library_file, include_path=None, library_path=None, cache_path=None):
        self.header_files = to_list(header_files)
        self.library_file = library_file
        self.include_path = include_path or os.curdir
        self.library_path = library_path or os.curdir
        self.cache_path = cache_path or './var'

        cache_key = u'_'.join(self.header_files) + '.pyclibrary'
        self.cache_file = os.path.join(self.cache_path, cache_key)

        logger.info('Setting up library "{}" with headers "{}"'.format(self.library_file, ', '.join(self.header_files)))

        self.setup()
        self.parse()
        self.load()

    def setup(self):

        # counter "ValueError: number of bits invalid for bit field"
        monkeypatch_pyclibrary_ctypes_struct()

        # register header- and library paths
        # https://pyclibrary.readthedocs.org/en/latest/get_started/configuration.html#specifying-headers-and-libraries-locations
        # TODO: this probably acts on a global basis; think about it
        if self.include_path:
            add_header_locations([self.include_path])
        if self.library_path:
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
        if not (CParser._init or CLibrary._init):
            auto_init(extra_types=types)

    def parse(self):
        # use an improved CParser which can grok/skip more constructor flavours
        self.parser = CParserEnhanced(self.header_files, cache=self.cache_file)

    def load(self):
        self.clib = CLibrary(self.library_file, self.parser, prefix='Lib_', lock_calls=False, convention='cdll', backend='ctypes')

    def struct_names(self):
        return self.parser.defs['structs'].keys()

    @classmethod
    def from_header(cls, include_path=None, header_files=None):
        cache_dir = user_cache_dir('lst', 'kotori')
        if not os.path.isdir(cache_dir): os.makedirs(cache_dir)
        library = LibraryAdapter(
            header_files, cls.compile(include_path, header_files),
            include_path=include_path, library_path=include_path,
            cache_path=cache_dir)
        return library

    @classmethod
    def compile(cls, include_path, header_files):
        """
        compiler := /opt/local/bin/g++-mp-5
        cppflags := -std=c++11
        define INCLUDE
            -I.
        endef
        """
        #$(compiler) $(cppflags) $(INCLUDE) -shared -fPIC -lm -o h2m_structs.so h2m_structs.h

        library_file = header_files[0].rstrip('.h') + '.so'

        library_file = os.path.join(include_path, library_file)
        source_files = map(lambda header_file: os.path.join(include_path, header_file), header_files)

        #command = 'g++ -I{include_path} -shared -fPIC -lm -o {library_file} {source_files}'.format(**locals())
        source_files = ' '.join(source_files)

        # TODO: make compiler configurable
        command = '/opt/local/bin/g++-mp-5 -std=c++11 -shared -fPIC -lm -o {library_file} {source_files}'.format(**locals())

        logger.info(slm('Compiling library: {}'.format(command)))
        retval = os.system(command)
        if retval == 0:
            logger.info('Successfully compiled {}'.format(library_file))
            return library_file
        else:
            msg = 'Failed compiling library {}'.format(library_file)
            logger.error(msg)
            raise ValueError(msg)


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

    def __repr__(self):
        return "<StructAdapter '{name}' object at {id}>".format(name=self.name, id=hex(id(self)))

    def print_schema(self):
        width = 84

        def print_header(text):
            print '-' * width
            print text.center(width)
            print '-' * width
            print

        print_header('struct "{}"'.format(self.name))

        print 'Header information'
        print
        print tabulate(self.ast_members_repr(), headers=['name', 'type', 'default', 'bitfield'])
        print; print

        print 'Library information'
        print
        print tabulate(self.lib_fields_repr(), headers=['name', 'type', 'symbol', 'field', 'bitfield'])
        print; print

        print 'Representations'
        print
        print tabulate(self.lib_binary_repr(), headers=['kind', 'representation'])
        print; print

    def ast_members_repr(self):

        def ast_type_repr(t):
            type_qual_str = ('' if not any(t.type_quals) else
                             ', type_quals='+repr(t.type_quals))
            return (', '.join(map(str, t)) + type_qual_str)

        members = []
        for member in self.ast().members:
            member_length = len(member)
            bitfield = None
            if member_length == 3:
                name, type, default = member
            elif member_length == 4:
                name, type, default, bitfield = member
            else:
                raise ValueError("Don't know how to handle ast members with length={}".format(member_length))

            # use name of type object
            type = ast_type_repr(type)

            entry = (name, type, default, bitfield)
            members.append(entry)

        return members

    def lib_fields_repr(self):
        fields = []
        o = self.obj()
        for field_item in o._fields_:

            field_length = len(field_item)
            bitfield = None
            if field_length == 2:
                name, ctype = field_item
            elif field_length == 3:
                name, ctype, bitfield = field_item
            else:
                raise ValueError("Don't know how to handle lib fields with length={}".format(field_length))

            # use name of ctypes object
            ctype_name = ctype.__name__
            symbol = ctype._type_

            # get ctypes Field object
            field = getattr(o, name)

            entry = (name, ctype_name, symbol, str(field), bitfield)
            fields.append(entry)

        return fields

    def lib_binary_repr(self):
        payload = self.create()._dump_()
        return self.binary_reprs(payload)

    @staticmethod
    def binary_reprs(payload):
        reprs = [
            ('hex',     '0x' + hexlify(payload)),
            ('decimal', map(ord, payload)),
            ('bytes',   repr(payload)),
        ]
        return reprs


class StructRegistry(object):

    def __init__(self, library):
        self.library = library

        # dictionary of structs, by name
        self.structs = {}

        self.build()

    def build(self):
        for name in self.library.struct_names():
            logger.debug('Rolling in struct "{}"'.format(name))
            self.register_adapter(name)

    def register_adapter(self, name):
        # store adapter object by name
        adapter = StructAdapter(name, self.library)
        self.structs[name] = adapter
        return adapter

    def get(self, name):
        return self.structs[name]

    def get_by_id(self, struct_id):
        try:
            return self.structs_by_id[struct_id]
        except KeyError:
            logger.error('Struct with id {} ({}) not registered'.format(struct_id, hex(struct_id)))
            sys.exit(1)

    def create(self, name, **attributes):
        return self.get(name).create(**attributes)

    @classmethod
    def to_dict(cls, struct):
        # TODO: maybe refactor to struct._dict_
        fieldnames = [field[0] for field in struct._fields_]
        d = OrderedDict()
        for fieldname in fieldnames:
            d[fieldname] = getattr(struct, fieldname)
        return d

    @classmethod
    def pprint(cls, struct, format='pprint'):
        # TODO: maybe refactor to struct._pprint_
        name = struct._name_()
        payload = struct._dump_()
        payload_hex = hexlify(payload)
        payload_data = list(cls.to_dict(struct).items())

        if format == 'pprint':
            print 'name:', name
            print 'hex: ', payload_hex
            pprint(payload_data, indent=4, width=42)

        elif format == 'tabulate-plain':
            seperator = ('----', '')
            output = [
                seperator,
                ('name', name),
                seperator,
            ]
            output += StructAdapter.binary_reprs(payload)
            output += [seperator]
            output += payload_data
            print tabulate(output, tablefmt='plain')

            #print tabulate(list(meta.items()), tablefmt='plain')
            #print tabulate(payload_data, missingval='n/a', tablefmt='simple')

        else:
            raise ValueError('Unknown format "{}" for pretty printer'.format(format))



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
            logger.warning('Struct "{}" has ID "{}", but this ID is already mapped to struct "{}", '\
                           'please check if struct provides reasonable default values for attribute "ID"'.format(name, struct_id, name_owner))
        else:
            logger.debug('Struct "{}" mapped to ID "{}"'.format(name, struct_id))
            self.structs_by_id[struct_id] = adapter
