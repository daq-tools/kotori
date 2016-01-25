# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import logging
from docopt import docopt
from kotori.configuration import get_configuration, get_configuration_file, configparser_to_dict, augment_configuration
from kotori.vendor.lst.application import setup_binary_message_adapter
from kotori.vendor.lst.commands import lst_message, setup_logging
from kotori.version import __VERSION__

logger = logging.getLogger(__name__)

APP_NAME = 'lst-message ' + __VERSION__

def message():
    """
    Usage:
      lst-message list-channels                    [--config etc/kotori.ini]
      lst-message <channel>  decode     <payload>  [--config etc/kotori.ini] [--debug]
      lst-message <channel>  transform  <payload>  [--config etc/kotori.ini] [--debug]
      lst-message <channel>  send       <payload>  --target=udp://localhost:8888 [--config etc/kotori.ini]
      lst-message <channel>  info       <name>     [--config etc/kotori.ini] [--debug]
      lst-message --version
      lst-message (-h | --help)

    Options:
      --config etc/kotori.ini   Use specified configuration file, otherwise try KOTORI_CONFIG environment variable
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen
    """

    # parse command line arguments
    options = docopt(message.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    debug = options.get('--debug')
    channel = options.get('<channel>')

    # setup logging
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # load configuration
    config_file = get_configuration_file(options.get('--config'))
    config = get_configuration(config_file)

    # serialize section-based ConfigParser contents into nested dict
    config = configparser_to_dict(config)
    augment_configuration(config)

    if options.get('list-channels'):
        channel_names = config['lst']['channels']
        print 'Channel names:'
        print
        print '\n'.join(channel_names)
        sys.exit()

    # activate/mount application
    # TODO: overfaul _active_ mechanics
    application_name = 'lst-' + channel
    try:
        config['_active_'] = config[application_name]
    except KeyError:
        logger.error('Application "{application_name}" not in configuration file "{config_file}"'.format(**locals()))

    # initialize library, setup BinaryMessageAdapter
    adapter = setup_binary_message_adapter(config)

    # dispatch to generic message decoding
    lst_message(adapter, options)
