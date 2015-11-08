# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import logging
from docopt import docopt, DocoptExit
from kotori.vendor.lst.h2m.util import setup_logging, setup_h2m_structs
from kotori.vendor.lst.message import BinaryMessageAdapter

APP_NAME = 'h2m-message 0.1.0'

messenger = None

def h2m_message_cmd():
    """
    Usage:
      h2m-message decode <payload> [--debug]
      h2m-message info   <name>    [--debug]
      h2m-message --version
      h2m-message (-h | --help)

    Options:
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    """
    options = docopt(h2m_message_cmd.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    debug = options.get('--debug')

    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # initialize "h2m_structs" library
    global messenger
    messenger = BinaryMessageAdapter(struct_registry=setup_h2m_structs())

    if options.get('decode'):
        payload = options.get('<payload>')
        struct = messenger.decode(payload)
        messenger.pprint(struct)

    elif options.get('info'):
        name = options.get('<name>')
        struct_adapter = messenger.struct_registry.get(name)
        struct_adapter.print_schema()
