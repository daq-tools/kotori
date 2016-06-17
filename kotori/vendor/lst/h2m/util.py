# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
from appdirs import user_cache_dir
from kotori.daq.intercom.c import LibraryAdapter, StructRegistryByID
#from kotori.daq.intercom.cffi_adapter import LibraryAdapterCFFI

def setup_h2m_structs_pyclibrary():
    cache_dir = os.path.join(user_cache_dir('kotori'), 'lst')
    if not os.path.isdir(cache_dir): os.makedirs(cache_dir)
    lib_dir = os.path.join(os.path.dirname(__file__), 'cpp')
    library = LibraryAdapter(u'h2m_structs.h', u'h2m_structs.so', include_path=lib_dir, library_path=lib_dir, cache_path=cache_dir)
    struct_registry = StructRegistryByID(library)
    return struct_registry

def setup_h2m_structs_cffi():
    cache_dir = os.path.join(user_cache_dir('kotori'), 'lst')
    if not os.path.isdir(cache_dir): os.makedirs(cache_dir)
    lib_dir = os.path.join(os.path.dirname(__file__), 'cpp')
    library = LibraryAdapterCFFI(u'h2m_structs.h', u'h2m_structs.so', include_path=lib_dir, library_path=lib_dir, cache_path=cache_dir)
    struct_registry = StructRegistryByID(library)
    return struct_registry

setup_h2m_structs = setup_h2m_structs_pyclibrary
