# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import re
from collections import OrderedDict
from cornice.util import to_list
from pprint import pprint
from binascii import hexlify
from tabulate import tabulate
from appdirs import user_cache_dir
from ctypes import c_uint8, c_uint16, c_uint32, c_int8, c_int16, c_int32
from pyclibrary.c_parser import CParser
from pyclibrary import CLibrary, auto_init
from pyclibrary.utils import add_header_locations, add_library_locations
from sympy.core.sympify import sympify
from twisted.logger import Logger
from kotori.daq.intercom.pyclibrary_ext.c_parser import CParserEnhanced
from kotori.daq.intercom.pyclibrary_ext.backend_ctypes import monkeypatch_pyclibrary_ctypes_struct
from kotori.util.common import slm

logger = Logger()

class LibraryAdapter(object):

    def __init__(self, header_files, library_file, include_path=None, library_path=None, cache_path=None):
        self.header_files = to_list(header_files)
        self.library_file = library_file
        self.include_path = include_path or os.curdir
        self.library_path = library_path or os.curdir
        self.cache_path = cache_path or './var'

        self.include_path = os.path.abspath(self.include_path)
        self.library_path = os.path.abspath(self.library_path)

        cache_key = \
            self.include_path.replace('/', '_') + \
            u'-' + \
            u'_'.join(self.header_files) + \
            u'.pyclibrary'
        self.cache_file = os.path.join(self.cache_path, cache_key)

        logger.info('Setting up library "{}" with headers "{}", cache file is "{}"'.format(
            self.library_file, ', '.join(self.header_files), self.cache_file))

        # holding the library essentials
        self.parser = None
        self.clib = None
        self.annotations = None

        self.setup()
        self.parse()
        self.parse_annotations()
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

        # TODO: this probably acts on a global basis; think about it
        if not (CParser._init or CLibrary._init):
            auto_init(extra_types=types)

    def parse(self):
        # use an improved CParser which can grok/skip more constructor flavours
        self.parser = CParserEnhanced(self.header_files, cache=self.cache_file)

    def parse_annotations(self):
        """
        Grok annotations like::

            // name=heading; expr=hdg * 20; unit=degrees
        """

        # compute list of source files (.h) with absolute paths
        source_files = [os.path.join(self.include_path, header_file) for header_file in self.header_files]

        # parse and compute annotations
        self.annotations = AnnotationParser(source_files, cache=self.cache_file + '.anno')

    def load(self):
        self.clib = CLibrary(self.library_file, self.parser, prefix='Lib_', lock_calls=False, convention='cdll', backend='ctypes')

    def struct_names(self):
        return list(self.parser.defs['structs'].keys())

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

        # compute list of source files (.h) with absolute paths
        source_files = [os.path.join(include_path, header_file) for header_file in header_files]
        source_files = cls.augment_sources(source_files)
        source_files = ' '.join(source_files)

        # compute absolute path to library (.so) file
        library_file = header_files[0].rstrip('.h') + '.so'
        library_file = os.path.join(include_path, library_file)

        # assemble compiler command
        compiler = cls.find_compiler()
        if not compiler:
            raise ValueError('Could not find compiler')
        command = '{compiler} -std=c++11 -shared -fPIC -lm -o {library_file} {source_files}'.format(**locals())

        # run compile command
        logger.info(slm('Compiling: {}'.format(command)))
        retval = os.system(command)
        if retval == 0:
            logger.info(slm('Successfully compiled library "{library_file}" from "{source_files}"'.format(**locals())))
            return library_file
        else:
            msg = 'Failed compiling library "{library_file}" from "{source_files}"'.format(**locals())
            logger.error(slm(msg))
            raise ValueError(msg)

    @classmethod
    def find_compiler(cls):
        # TODO: make compiler configurable via ini file
        # TODO: investigate problem with /usr/bin/clang++: "clang: error: cannot specify -o when generating multiple output files"
        compilers = ['/opt/local/bin/g++-mp-4.7', '/usr/bin/g++']
        for compiler in compilers:
            if os.path.isfile(compiler):
                return compiler

    @classmethod
    def augment_sources(cls, source_files):
        """
        Augments source files and puts them under /tmp:
        - Automatically add ``#include "stdint.h"`` (required for types ``uint8_t``, etc.)
          and remove ``#include "mbed.h"`` (croaks on Intel)
        """
        source_files_augmented = []
        for source_file in source_files:

            # split source file into parts ...
            dirname = os.path.dirname(source_file)
            basename = os.path.basename(source_file)
            name, ext = os.path.splitext(basename)

            # and compute augmented file name
            name_intel = name
            name_intel += '_intel'
            name_intel += ext
            source_file_augmented = os.path.join(dirname, name_intel)

            # augment sourcecode
            source_payload = cls.augment_source(source_file)

            # write augmented file
            open(source_file_augmented, 'w').write(source_payload)
            source_files_augmented.append(source_file_augmented)

        return source_files_augmented

    @classmethod
    def augment_source(cls, source_file):
        """
        No matter if there's a ``#include "mbed.h"``, make sure it gets removed.
        Also make sure that there is a single ``#include "stdint.h"``.
        """
        payload = open(source_file).read()
        if re.search('^#include "stdint.h"', payload, re.MULTILINE):
            amendment = ''
        else:
            amendment = '#include "stdint.h"'

        if re.search('^#include "mbed.h"', payload, re.MULTILINE):
            payload = payload.replace('#include "mbed.h"', amendment)
        else:
            if amendment:
                payload = amendment + '\n' + payload
        return payload


class AnnotationParser(object):

    def __init__(self, source_files, cache=None):

        self.source_files = source_files

        # keep all parsed information here
        self.info = {'structs': {}}

        # parse all annotations
        self.parse()

    def parse(self):
        """
        Parse rule annotations like::

                int16_t  hdg                ;//6        /* @rule: name=heading; expr=hdg * 20; unit=degrees */

        """

        # e.g. "typedef struct struct_position         // added 06.03.2014 C.L."
        struct_head_pattern  = re.compile('^.*struct\s+([\w]+).*?$')

        # e.g. "/* @rule: name=heading; expr=hdg * 20; unit=degrees */"
        rule_extract_pattern = re.compile('^.*name=(?P<name>\w+?);.*expr=(?P<expression>.+?);.*unit=(?P<unit>\w+).*$')

        # e.g. "   int16_t  hdg                ;"
        original_fieldname_pattern = re.compile('^.*?(?P<type>[\w]+)\s+(?P<name>[\w]+).*;.*$')

        for source_file in self.source_files:

            struct_name = None
            with open(source_file) as f:
                for line in f.readlines():
                    line = line.strip()

                    # check for beginning of struct
                    m = struct_head_pattern.match(line)
                    if m:
                        struct_name = m.group(1)

                    # check for transformation rule annotation
                    if '@rule:' in line:
                        m = rule_extract_pattern.match(line)
                        if m:
                            rule = m.groupdict()
                            if 'expression' in rule:
                                rule['expression_sympy'] = sympify(rule['expression'])

                            # parse original field name to map against
                            m = original_fieldname_pattern.match(line)
                            if m:
                                vanilla_field = m.groupdict()
                                field_name = vanilla_field['name']
                                self.info['structs'].setdefault(struct_name, {})
                                self.info['structs'][struct_name][field_name] = rule

        #pprint(self.info)

    def get_struct_rules(self, struct_name):
        return self.info['structs'].get(struct_name, {})

    def get_struct_rule(self, struct_name, field_name):
        struct_rules = self.get_struct_rules(struct_name)
        return struct_rules.get(field_name)


class StructAdapter(object):

    def __init__(self, name, library):
        self.name = name
        self.library = library
        self.parser = self.library.parser
        self.clib = self.library.clib
        self.annotations = self.library.annotations

    def ast(self):
        return self.parser.defs['structs'][self.name]

    def obj(self):
        return self.clib('structs', self.name)

    def create(self):
        """
        Create and initialize ctypes struct.
        """
        # wrapper class from pyclibrary.backend_ctypes
        obj_wrapper = self.obj()

        # <ctypes struct 'struct_foo'>
        obj = obj_wrapper()

        # initialize struct content
        self.initialize(obj)

        return obj

    def initialize(self, obj):
        """
        Initialize struct instance with initializer data
        """
        data = self._get_initializer_data()
        if data:
            bytes = ''.join(map(chr, data))
            obj._load_(bytes)

    def _get_initializer_data(self):
        """
        Nasty hack to get proper initializer data from CParser results.

        This works by traversing the CParser result nodes from the variable ``position``
        back to the struct ``struct_position`` to correlate struct with initializer data.

        Example struct declaration::

            struct struct_position
            {
                uint8_t  length             ;//1
                uint8_t  ID                 ;//2
                // ...
            } position = {9,1};

        Obviously, this will only work for singletons, where each struct used is instantiated only once.
        You have been warned.
        """
        for key, value in self.parser.defs['variables'].items():
            data, type = value
            type_spec = 'struct ' + self.name
            if type_spec == type.type_spec:
                return data

        # don't log, this would be triggered erroneously when using equal-style-initializers
        #logger.warn('Could not find initialization data for struct "{}"'.format(self.name))

    def __repr__(self):
        return "<StructAdapter '{name}' object at {id}>".format(name=self.name, id=hex(id(self)))

    def print_schema(self):
        width = 84

        def print_header(text):
            print('-' * width)
            print(text.center(width))
            print('-' * width)
            print()

        print_header('struct "{}"'.format(self.name))

        print('Header information')
        print()
        print(tabulate(self.ast_members_repr(), headers=['name', 'type', 'default', 'bitfield']))
        print(); print()

        print('Library information')
        print()
        print(tabulate(self.lib_fields_repr(), headers=['name', 'type', 'symbol', 'field', 'bitfield']))
        print(); print()

        print('Transformation rules')
        print()
        print(tabulate(self.annotations_repr(), headers=['name-real', 'name-human', 'expression', 'expression-sympy', 'unit']))
        print(); print()

        print('Representations')
        print()
        print(tabulate(self.lib_binary_repr(), headers=['kind', 'representation']))
        print(); print()

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

    def annotations_repr(self):
        entries = []
        annos = self.annotations.get_struct_rules(self.name)
        if annos:
            for fieldname, rule in annos.items():
                entry = (fieldname, rule['name'], rule['expression'], rule['expression_sympy'], rule['unit'])
                entries.append(entry)
        return entries

    @staticmethod
    def binary_reprs(payload):
        reprs = [
            ('hex',     '0x' + hexlify(payload)),
            ('decimal', list(map(ord, payload))),
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
            msg = 'Struct with id {} ({}) not registered.'.format(struct_id, hex(struct_id))
            logger.error(slm(msg))
            raise KeyError(msg)

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
    def pprint(cls, struct, data=None, format='pprint'):
        # TODO: maybe refactor to struct._pprint_
        name = struct._name_()
        payload = struct._dump_()
        payload_hex = hexlify(payload)
        if data:
            payload_data = list(data.items())
        else:
            payload_data = list(cls.to_dict(struct).items())

        if format == 'pprint':
            print('name:', name)
            print('hex: ', payload_hex)
            pprint(payload_data, indent=4, width=42)

        elif format == 'tabulate-plain':
            separator = ('----', '')
            output = [
                separator,
                ('name', name),
                separator,
            ]
            output += StructAdapter.binary_reprs(payload)
            output += [separator]
            output += payload_data
            print(tabulate(output, tablefmt='plain'))

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
        if struct_id in self.structs_by_id:
            o_a = self.structs_by_id[struct_id]
            name_owner = o_a.name
            logger.warn('Struct "{}" has ID "{}", but this ID is already mapped to struct "{}", '\
                           'please check if struct provides reasonable default values for attribute "ID"'.format(name, struct_id, name_owner))
        else:
            logger.debug('Struct "{}" mapped to ID "{}"'.format(name, struct_id))
            self.structs_by_id[struct_id] = adapter

    def get_metadata(self):
        metadata = []
        for index in sorted(self.structs_by_id.keys()):
            struct = self.structs_by_id[index]
            members = struct.ast_members_repr()
            fieldnames = [member[0] for member in members]
            entry = OrderedDict()
            entry['id'] = index
            entry['name'] = struct.name
            entry['# structs'] = len(fieldnames)
            metadata.append(entry)
        return metadata
