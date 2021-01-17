# -*- coding: utf-8 -*-
"""
Kotori is a data acquisition, routing and graphing toolkit
Copyright (C) 2014-2021 Andreas Motl, <andreas@getkotori.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from bunch import Bunch
from docopt import docopt
from pkgutil import extend_path
from twisted.internet import reactor
from twisted.logger import Logger, LogLevel
from kotori.core import APP_NAME, KotoriBootloader
from kotori.frontend.server import boot_frontend
from kotori.util.common import setup_logging
from kotori.util.logger import startLogging
from kotori.util.configuration import get_configuration, get_configuration_file, apply_default_settings

__path__ = extend_path(__path__, __name__)

__doc__ = APP_NAME + """

Usage:
  kotori [--config etc/development.ini] [--debug-io] [--debug-mqtt] [--debug-mqtt-driver] [--debug-influx] [--debug] [--debug-vendor vendor42,vendor-xyz]
  kotori --version
  kotori (-h | --help)

Options:
  --config etc/kotori.ini   Start Kotori with configuration file
  --version                 Show version information
  --debug-io                Enable debug messages for IO subsystem
  --debug-mqtt              Enable debug messages for MQTT
  --debug-mqtt-driver       Enable debug messages for MQTT driver
  --debug-influx            Enable debug messages for InfluxDB
  --debug                   Generic debug flag passed down to other subsystems
  --debug-vendor vendor42   Debug flag passed down to given vendor subsystems
  -h --help                 Show this screen

"""

log = Logger()


def boot(options=None):

    options = options or {}
    options.setdefault('--debug', False)
    options.setdefault('--debug_mqtt', False)
    options.setdefault('--debug_mqtt_driver', False)
    options.setdefault('--debug_io', False)
    options.setdefault('--debug_influx', False)

    setup_logging()
    log.info(u'Starting ' + APP_NAME)

    # Read settings from configuration file
    configfile = get_configuration_file(options['--config'])
    log.info("Using configuration file {configfile}", configfile=configfile)
    settings = get_configuration(configfile)

    # Apply default settings
    apply_default_settings(settings)

    # Merge command line options into settings
    settings.setdefault('options', Bunch())
    for key, value in options.items():
        key = key.lstrip(u'--')
        key = key.replace(u'-', u'_')
        settings.options[key] = value

    # Setup the logging subsystem
    log_level = 'info'
    if settings.options.debug:
        log_level = 'debug'
    startLogging(settings, stream=sys.stderr, level=LogLevel.levelWithName(log_level))

    # Boot all enabled applications and vendors
    loader = KotoriBootloader(settings=settings)
    loader.boot_applications()
    loader.boot_vendors()

    # Boot web configuration GUI
    if 'config-web' in settings:
        boot_frontend(settings, debug=settings.options.debug)

    return loader


def run():

    # Read commandline options
    # TODO: Do it the Twisted way
    options = docopt(__doc__, version=APP_NAME)

    # Bootstrap the service.
    boot(options)

    # Enter Twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    run()
