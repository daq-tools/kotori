# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import shelve
import socket
from uuid import uuid4
from appdirs import user_data_dir
import json_store


class Singleton(object):
    """
    Singleton class by Duncan Booth.
    Multiple object variables refers to the same object.
    http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class ConfigStore(dict):

    store = None

    def __init__(self):
        if not ConfigStore.store:
            print "###################### ConfigStore init"
            self.app_data_dir = user_data_dir('kotori', 'elmyra')
            if not os.path.exists(self.app_data_dir):
                os.makedirs(self.app_data_dir)
            self.config_file = os.path.join(self.app_data_dir, 'config')
            ConfigStore.store = shelve.open(self.config_file, writeback=True)

    def has_key(self, key):
        return ConfigStore.store.has_key(key)

    def __getitem__(self, key):
        print 'ConfigStore.__getitem__'
        return ConfigStore.store[key]

    def __setitem__(self, key, value):
        print 'ConfigStore.__setitem__', key, value
        ConfigStore.store[key] = value
        ConfigStore.store.sync()


class BetterConfigStore(dict):

    store = None

    def __init__(self):
        if not BetterConfigStore.store:
            print "###################### ConfigStore init"
            self.app_data_dir = user_data_dir('kotori', 'elmyra')
            if not os.path.exists(self.app_data_dir):
                os.makedirs(self.app_data_dir)
            self.config_file = os.path.join(self.app_data_dir, 'config.json')
            BetterConfigStore.store = json_store.open(self.config_file)

    def has_key(self, key):
        return BetterConfigStore.store.has_key(key)

    def __getitem__(self, key):
        print 'BetterConfigStore.__getitem__'
        return BetterConfigStore.store[key]

    def __setitem__(self, key, value):
        print 'BetterConfigStore.__setitem__', key, value
        BetterConfigStore.store[key] = value
        BetterConfigStore.store.sync()


class NodeId(Singleton):

    config = None
    NODE_ID = 'NODE_UNKNOWN'

    def __init__(self):
        if not self.config:
            self.config = ConfigStore()
        if not self.config.has_key('uuid'):
            self.config['uuid'] = str(uuid4())
        self.NODE_ID = self.config['uuid']
        print "NODE ID:", self.NODE_ID

    def __str__(self):
        return str(self.NODE_ID)

def get_hostname():
    return socket.gethostname()
