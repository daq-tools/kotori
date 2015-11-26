# -*- coding: utf-8 -*-
# (c) 2014,2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import logging
from exceptions import ValueError
from ConfigParser import ConfigParser

logger = logging.getLogger()

def get_configuration(configfile):

    # read configuration
    config = ConfigParser()
    success = config.read([configfile, os.path.expanduser('~/.kotori.ini')])
    if success:
        logger.info('Read configuration files: {}'.format(success))
        #logger.info('config: {}'.format(config))
    else:
        msg = 'Could not read configuration file {}'.format(configfile)
        logger.error(msg)
        raise ValueError(msg)

    return config


def get_configuration_file(direct=None):

    # compute configuration file
    configfile = direct
    if not configfile:
        configfile = os.environ.get('KOTORI_CONFIG')
    logger.info('configfile: {}'.format(configfile))
    if not configfile:
        raise ValueError('No configuration file, either use --config=/path/to/kotori.ini or set KOTORI_CONFIG environment variable')

    return configfile


def configparser_to_dict(config):
    # serialize section-based ConfigParser contents into nested dict
    if isinstance(config, ConfigParser):
        config_dict = {}
        for section in config.sections():
            config_dict[section] = dict(config.items(section))
        return config_dict
    else:
        return config


def augment_configuration(config_dict):
    # augment configuration
    config_dict['lst']['channels'] = map(str.strip, config_dict['lst']['channels'].split(','))
    return config_dict