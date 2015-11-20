# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import logging
from pprint import pprint
from docopt import docopt
from kotori import get_configuration
from kotori.util import configparser_to_dict
from kotori.vendor.lst.application import setup_binary_message_adapter
from kotori.vendor.lst.commands import lst_message, setup_logging

logger = logging.getLogger(__name__)

APP_NAME = 'h2m-message 0.1.0'

def h2m_message_cmd():
    """
    Usage:
      h2m-message decode <payload> [--debug]
      h2m-message send   <payload> --target=udp://localhost:8888
      h2m-message info   <name>    [--debug]
      h2m-message --version
      h2m-message (-h | --help)

    Options:
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    """

    # parse command line arguments
    options = docopt(h2m_message_cmd.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    debug = options.get('--debug')

    # setup logging
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # load configuration
    config = get_configuration('etc/development.ini')

    # serialize section-based ConfigParser contents into nested dict
    config = configparser_to_dict(config)

    # activate/mount "h2m" application
    config['_active_'] = config['lst-h2m']

    # initialize library, setup BinaryMessageAdapter
    adapter = setup_binary_message_adapter(config)

    # dispatch to generic message decoding
    lst_message(adapter, options)

