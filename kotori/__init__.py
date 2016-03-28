# -*- coding: utf-8 -*-
# (c) 2014-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
from bunch import Bunch
from docopt import docopt
from pkgutil import extend_path
from twisted.internet import reactor
from twisted.logger import Logger, LogLevel
from kotori.configuration import get_configuration, get_configuration_file, read_list
from kotori.logger import startLogging
from kotori.frontend.server import boot_frontend
from .version import __VERSION__

__path__ = extend_path(__path__, __name__)

APP_NAME = 'Kotori version ' + __VERSION__
__doc__ = APP_NAME + """

Usage:
  kotori [--config etc/development.ini] [--debug-mqtt] [--debug-mqtt-driver] [--debug-influx]
  kotori --version
  kotori (-h | --help)

Options:
  --config etc/kotori.ini   Start Kotori with configuration file
  --version                 Show version information
  --debug-mqtt              Enable debug messages for MQTT
  --debug-influx            Enable debug messages for InfluxDB
  --debug-mqtt-driver       Enable debug messages for MQTT driver
  -h --help                 Show this screen

"""

log = Logger()

def run():

    log.info(APP_NAME)

    # Read commandline options
    # TODO: Do it the Twisted way
    options = docopt(__doc__, version=APP_NAME)
    debug = options.get('--debug', False)

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
    #log_level = 'debug' if debug else 'info'
    log_level = 'info'
    #log_level = 'debug'
    startLogging(settings, stream=sys.stderr, level=LogLevel.levelWithName(log_level))

    # Boot all enabled vendors
    vendors = read_list(settings.vendors.enable)
    log.info('Enabling vendors {vendors}', vendors=vendors)

    if 'hydro2motion' in vendors:
        from kotori.vendor.hydro2motion.database.influx import h2m_boot_influx_database
        from kotori.vendor.hydro2motion.network.udp import h2m_boot_udp_adapter
        from kotori.vendor.hydro2motion.web.server import boot_web
        boot_web(settings, debug=debug)
        h2m_boot_udp_adapter(settings, debug=debug)
        h2m_boot_influx_database(settings)

    if 'hiveeyes' in vendors:
        from kotori.vendor.hiveeyes.application import hiveeyes_boot
        hiveeyes_boot(settings, debug=debug)

    if 'lst' in vendors:
        from kotori.vendor.lst.application import lst_boot
        lst_boot(settings)

    # Boot web configuration GUI
    if 'config-web' in settings:
        boot_frontend(settings, debug=debug)

    # Enter Twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    run()
