# -*- coding: utf-8 -*-
# (c) 2014-2021 Andreas Motl, <andreas@getkotori.org>
import os
import logging
from configparser import ConfigParser
from glob import glob
from bunch import Bunch
from cornice.util import to_list

log = logging.getLogger()


def get_configuration_file(configfile=None):

    # Compute path to configuration file.
    if not configfile:
        configfile = os.environ.get('KOTORI_CONFIG')

    if not configfile:
        raise ValueError('No configuration file given, '
                         'either use --config=/path/to/kotori.ini or set KOTORI_CONFIG environment variable')

    log.info('Root configuration file is {}'.format(configfile))
    return configfile


def get_configuration(*args):
    config_files = []
    # TODO: Only use when logged in interactively?
    config_files += [os.path.expanduser('~/.kotori.ini')]
    config_files += list(args)
    log.info('Requested configuration files: {}'.format(make_list(config_files)))
    config, used = read_config(config_files, kind=Bunch)
    if config:
        if 'main' in config and 'include' in config.main:
            includes = read_list(config.main.include)
            for include in includes:
                if '*' in include or '?' in include:
                    config_files += glob(include)
                else:
                    config_files.append(include)
            log.info('Expanded configuration files:  {}'.format(make_list(config_files)))
            config, used = read_config(config_files, kind=Bunch)
        log.info('Used configuration files:      {}'.format(make_list(used)))
        return config
    else:
        msg = u'Could not read settings from configuration files: {}'.format(config_files)
        log.critical(msg)
        raise ValueError(msg)


def read_config(configfiles, kind=None):
    configfiles_requested = to_list(configfiles)
    config = ConfigParser()
    configfiles_used = config.read(configfiles_requested)
    settings = convert_config(config, kind=kind)
    return settings, configfiles_used


def convert_config(config, kind=None):
    """
    Serialize section-based ConfigParser contents
    into nested dict or other dict-like thing.
    """
    kind = kind or dict
    if isinstance(config, ConfigParser):
        config_dict = kind()
        for section in config.sections():
            config_dict[section] = kind(config.items(section))
        return config_dict
    else:
        return config


def read_list(string, separator=u',', empty_elements=True):
    data = list(map(str.strip, string.split(separator)))
    if empty_elements == False:
        data = [x for x in data if bool(x)]
    return data


def make_list(items, separator=u', '):
    return separator.join(items)


def apply_default_settings(settings):

    # MQTT setting defaults
    settings.mqtt.setdefault('host', u'localhost')
    settings.mqtt.setdefault('port', u'1883')
    settings.mqtt.setdefault('debug', u'false')

