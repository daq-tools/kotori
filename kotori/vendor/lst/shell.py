# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import logging
from bunch import Bunch
from docopt import docopt
from kotori.version import __VERSION__
from kotori.util.common import setup_logging
from kotori.util.configuration import get_configuration, get_configuration_file
from kotori.vendor.lst.application import setup_binary_message_adapter
from kotori.vendor.lst.commands import lst_channels, lst_message, sanitize_channel_label, compute_channel_label

logger = logging.getLogger(__name__)

APP_NAME = 'lst-message ' + __VERSION__

def message():
    """
    Usage:
      lst-message list-channels                    [--config etc/kotori.ini] [--debug]
      lst-message <channel>  decode     <payload>  [--config etc/kotori.ini] [--debug]
      lst-message <channel>  transform  <payload>  [--config etc/kotori.ini] [--debug]
      lst-message <channel>  send       <payload>  --target=udp://localhost:8888 [--config etc/kotori.ini]
      lst-message <channel>  info       [<name>]   [--config etc/kotori.ini] [--debug]
      lst-message --version
      lst-message (-h | --help)

    Options:
      --config etc/kotori.ini   Use specified configuration file, otherwise try KOTORI_CONFIG environment variable
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    Examples:

      # Initialize environment with path to configuration file, either on development or production
      export KOTORI_CONFIG=`pwd`/etc/development.ini
      export KOTORI_CONFIG=/etc/kotori/kotori.ini

      # Show list of channels
      lst-message list-channels

      # Display list of structs for channel "h2m"
      lst-message h2m info

      # Display details about struct "struct_fuelcell_r" in channel "h2m"
      lst-message h2m info struct_fuelcell_r

      # Decode message for channel "h2m"
      lst-message h2m decode 0x05022a0021

      # Send message to channel "h2m"
      lst-message h2m send 0x05022a0021 --target=udp://localhost:8888

    """

    # parse command line arguments
    options = docopt(message.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    debug = options.get('--debug')

    # setup logging
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # load configuration
    config_file = get_configuration_file(options.get('--config'))
    config = get_configuration(config_file)

    # first command
    if options.get('list-channels'):
        lst_channels(config)
        sys.exit()

    # activate/mount application representing selected channel
    channel_label = options.get('<channel>')
    channel_name  = sanitize_channel_label(channel_label)
    if channel_name == channel_label:
        channel_label = compute_channel_label(channel_name)
    channel = Bunch(
        name  = channel_name,
        label = channel_label)
    # TODO: overhaul _active_ mechanics
    try:
        config['_active_'] = config[channel.label]
        channel.settings = config['_active_']
    except KeyError:
        logger.error('Channel configuration object "{channel_label}" not found'.format(channel_label = channel.label))
        raise

    # initialize library, setup BinaryMessageAdapter
    adapter = setup_binary_message_adapter(config)

    # dispatch to generic message decoding
    lst_message(channel, adapter, options)
