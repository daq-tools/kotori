# -*- coding: utf-8 -*-
# (c) 2014-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
from pkgutil import extend_path
from twisted.internet import reactor
from twisted.logger import Logger, LogLevel
from kotori.configuration import get_configuration, get_configuration_file
from kotori.logger import startLogging
from kotori.io.master.server import boot_master
from kotori.io.node.nodeservice import boot_node
from kotori.frontend.server import boot_frontend
from kotori.vendor.hydro2motion.database.influx import h2m_boot_influx_database
from kotori.vendor.hydro2motion.network.udp import h2m_boot_udp_adapter
from kotori.vendor.hydro2motion.web.server import boot_web
from kotori.vendor.hiveeyes.application import hiveeyes_boot
from kotori.vendor.lst.application import lst_boot
from kotori.util import slm
from .version import __VERSION__

__path__ = extend_path(__path__, __name__)

APP_NAME = 'Kotori version ' + __VERSION__
__doc__ = APP_NAME + """

Usage:
  kotori [--config etc/development.ini] [--debug]
  kotori --version
  kotori (-h | --help)

Options:
  --config etc/kotori.ini   Start Kotori with configuration file
  --version                 Show version information
  --debug                   Enable debug messages
  -h --help                 Show this screen

"""
"""
deprecated:
  #kotori master [--debug]
  #kotori node --master=<> [--debug]
"""
from docopt import docopt

logger = Logger()

def run():

    logger.info(APP_NAME)

    options = docopt(__doc__, version=APP_NAME)
    logger.info('options: {}'.format(slm(dict(options))))
    debug = options.get('--debug', False)
    logger.info("debug: {}".format(debug))

    log_level = 'debug' if debug else 'info'
    startLogging(sys.stderr, level=LogLevel.levelWithName(log_level))

    config_file = get_configuration_file(options['--config'])
    config = get_configuration(config_file)

    # defaults
    websocket_uri = unicode(config.get('wamp', 'listen'))
    http_port_v2 = int(config.get('kotori-daq', 'http_port'))

    # run master and web gui
    if 'master' in options:
        boot_master(websocket_uri, debug)
        #boot_web(35000, '', debug)
        #boot_udp_adapter(udp_port, debug)

    # run node and web gui only, using a remote master
    if 'node' in options:
        websocket_uri = options['--master']
        #boot_web(35000, websocket_uri, debug)
        boot_node(websocket_uri, debug)
        #boot_udp_adapter(udp_port, debug)

    # run master, node and web gui
    else:
        """
        boot_master(websocket_uri, debug=debug)
        boot_web(http_port, websocket_uri, debug=debug)
        boot_frontend(frontend_port, websocket_uri, debug=debug)
        boot_node(websocket_uri, debug=debug)
        boot_udp_adapter(udp_port, debug=debug)
        boot_sql_database(websocket_uri)
        boot_mongo_database(websocket_uri)
        boot_influx_database(websocket_uri)
        """

        # hydro2motion
        if config.has_section('hydro2motion'):
            http_port_v1 = int(config.get('hydro2motion', 'http_port'))

            boot_web(http_port_v1, websocket_uri, debug=debug)
            h2m_boot_udp_adapter(config, debug=debug)
            h2m_boot_influx_database(config)

        # hiveeyes
        if config.has_section('hiveeyes'):
            hiveeyes_boot(config, debug=debug)

        if config.has_section('lst-h2m'):
            lst_boot(config)

        # generic daq
        if config.has_section('kotori-daq'):
            boot_frontend(http_port_v2, websocket_uri, debug=debug)


    # now enter the Twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    run()
