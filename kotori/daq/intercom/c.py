# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import logging
from pprint import pprint
from cornice.util import to_list
from ctypes import c_int, c_uint, c_long, c_uint8, c_uint16, c_uint32
from pyclibrary import CLibrary, auto_init
from pyclibrary.utils import add_header_locations, add_library_locations
from pyclibrary.c_parser import Type, integer
from kotori.daq.intercom.pyclibrary_ext.c_parser import CParserEnhanced
from kotori.daq.intercom.pyclibrary_ext.backend_ctypes import monkeypatch_pyclibrary_ctypes_struct

#logging.basicConfig(level=logging.DEBUG)
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
        add_header_locations([self.include_path])
        add_library_locations([self.library_path])

        # define extra types suitable for embedded use
        types = {
            'uint8_t': c_uint8,
            'uint16_t': c_uint16,
            'uint32_t': c_uint32,
        }
        auto_init(extra_types=types)

    def parse(self):
        # use an improved CParser which can grok more constructor flavours
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
        self.structs = {}
        self.build()

    def build(self):
        for name in self.library.struct_names():
            self.structs[name] = StructAdapter(name, self.library)

    def get(self, name):
        return self.structs[name]

    def create(self, name, **attributes):
        return self.get(name).create(**attributes)


def main():

    curr_dir = os.curdir
    lib_dir = os.path.join(curr_dir, 'kotori', 'vendor', 'lst', 'client', 'cpp')
    cache_dir = os.path.join(curr_dir, 'var', 'cache')

    library = LibraryAdapter(u'h2m_structs.h', u'h2m_structs.so', include_path=lib_dir, library_path=lib_dir, cache_path=cache_dir)
    sr = StructRegistry(library)



    #values = struct_program.from_buffer_copy(b"\x01\x00\x00\x00\x00\x00\x00\x00")
    #print 'values:', values



    #clib = sa.clib


    #p = clib.struct_program(1, 2) #(abc=9)
    #p = clib.Tstruct_program() #(abc=9)

    #pprint(clib.struct_cap_r._objects)


    #c = clib.struct_cap_r #(abc=9)


    # create a "cap_r" struct and print attributes with default values
    print '-' * 42
    p = sr.create('struct_cap_r')
    print 'thing: ', p
    print 'length:', p.length
    print 'ID:    ', p.ID

    # create a "cap_r" struct overriding default values and print the relevant attributes
    print '-' * 42
    p = sr.create('struct_cap_r', ID=88)
    print 'thing: ', p
    print 'length:', p.length
    print 'ID:    ', p.ID


    # get lowlevel pyclibrary ctypes backend handle of "struct_program"
    print '-' * 42
    print 'struct_program (schema):'
    struct_program = sr.get('struct_program')
    pprint(struct_program)
    csp = struct_program.obj() #(abc=9)
    print 'thing:      ', csp
    print 'length:     ', csp.length
    print 'ID:         ', csp.ID
    print 'send_ser:   ', csp.send_ser
    print 'cfg_loaded: ', csp.cfg_loaded

    print '-' * 42
    print 'struct_program (instance):'
    print 'thing:      ', csp()
    print 'length:     ', csp().length
    print 'ID:         ', csp().ID


    # get lowlevel pyclibrary ctypes backend handle of "struct_cap_r"
    print '-' * 42
    c = sr.get('struct_cap_r').obj()
    print 'thing: ', c
    print 'length:', c.length
    print 'ID:    ', c.ID

    print 'FIELDS:'
    pprint(c._fields_)
    print 'DEFAULTS:'
    pprint(c._defaults_)


if __name__ == '__main__':
    main()
