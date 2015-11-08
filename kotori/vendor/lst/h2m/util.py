# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import logging
from kotori.daq.intercom.c import LibraryAdapter, StructRegistryByID

def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-25s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)

def setup_h2m_structs():
    cache_dir = os.path.join(os.curdir, 'var', 'cache')
    lib_dir = os.path.join(os.path.dirname(__file__), 'cpp')
    library = LibraryAdapter(u'h2m_structs.h', u'h2m_structs.so', include_path=lib_dir, library_path=lib_dir, cache_path=cache_dir)
    struct_registry = StructRegistryByID(library)
    return struct_registry
