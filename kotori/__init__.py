# -*- coding: utf-8 -*-
# (c) 2014-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
from bunch import Bunch
from docopt import docopt
from pkgutil import extend_path
from twisted.internet import reactor
from twisted.logger import Logger, LogLevel
from kotori.util import setup_logging
from kotori.core import APP_NAME, KotoriBootloader
from kotori.logger import startLogging
from kotori.configuration import get_configuration, get_configuration_file
from kotori.frontend.server import boot_frontend

__path__ = extend_path(__path__, __name__)

__doc__ = APP_NAME + """

Usage:
  kotori [--config etc/development.ini] [--debug-mqtt] [--debug-mqtt-driver] [--debug-influx] [--debug] [--debug-vendor vendor42,vendor-xyz]
  kotori --version
  kotori (-h | --help)

Options:
  --config etc/kotori.ini   Start Kotori with configuration file
  --version                 Show version information
  --debug-mqtt              Enable debug messages for MQTT
  --debug-influx            Enable debug messages for InfluxDB
  --debug-mqtt-driver       Enable debug messages for MQTT driver
  --debug                   Generic debug flag passed down to other subsystems
  --debug-vendor vendor42   Debug flag passed down to given vendor subsystems
  -h --help                 Show this screen

"""

log = Logger()

def run():

    setup_logging()
    log.info(u'Starting ' + APP_NAME)

    # Read commandline options
    # TODO: Do it the Twisted way
    options = docopt(__doc__, version=APP_NAME)

    # Read settings from configuration file
    configfile = get_configuration_file(options['--config'])
    log.info("Using configuration file {configfile}", configfile=configfile)
    settings = get_configuration(configfile)

    # Merge command line options into settings
    settings.setdefault('options', Bunch())
    for key, value in options.iteritems():
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

    # Enter Twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    run()
