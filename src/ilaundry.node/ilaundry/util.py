# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import shelve
from uuid import uuid4
from appdirs import user_data_dir


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

    def __init__(self):
        self.app_data_dir = user_data_dir('iLaundry', 'useeds')
        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)
        self.config_file = os.path.join(self.app_data_dir, 'config')
        self.store = shelve.open(self.config_file, writeback=True)

    def has_key(self, key):
        return self.store.has_key(key)

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value
        self.store.sync()


class NodeId(Singleton):

    config = None
    NODE_ID = 'NODE_UNKNOWN'

    def __init__(self):
        if not self.config:
            self.config = ConfigStore()
        if not self.config.has_key('uuid'):
            self.config['uuid'] = str(uuid4())
        self.NODE_ID = self.config['uuid']

    def __str__(self):
        return str(self.NODE_ID)
