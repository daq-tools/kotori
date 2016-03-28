# -*- coding: utf-8 -*-
# (c) 2014-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import logging
from bunch import Bunch
from cornice.util import to_list
from ConfigParser import ConfigParser

log = logging.getLogger()

def get_configuration(configfile):
    configfiles = [configfile, os.path.expanduser('~/.kotori.ini')]
    config = read_config(configfiles, kind=Bunch)
    if config:
        return config
    else:
        msg = u'Could not read settings from configuration files: {}'.format(configfiles)
        log.critical(msg)
        raise ValueError(msg)

def get_configuration_file(direct=None):

    # compute configuration file
    configfile = direct
    if not configfile:
        configfile = os.environ.get('KOTORI_CONFIG')
    log.info('configfile: {}'.format(configfile))
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


def read_list(string, separator=u','):
    return map(unicode.strip, string.split(separator))


def read_config(configfiles, kind=None):
    configfiles = to_list(configfiles)
    config = ConfigParser()
    config.read(configfiles)
    if kind is not None:
        settings = convert_config(config, kind=kind)
    else:
        settings = convert_config(config)

    return settings


def convert_config(config, kind=dict):
    # serialize section-based ConfigParser contents into
    # nested dict or other dict-like thing
    if isinstance(config, ConfigParser):
        config_dict = kind()
        for section in config.sections():
            config_dict[section] = kind(config.items(section))
        return config_dict
    else:
        return config
