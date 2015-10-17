# -*- coding: utf-8 -*-
# (c) 2014-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
from pkgutil import extend_path
from ConfigParser import ConfigParser
from twisted.internet import reactor
from twisted.python.log import startLogging
from twisted.logger import Logger
from kotori.master.server import boot_master
from kotori.node.nodeservice import boot_node
from kotori.web.server import boot_web
from kotori.hydro2motion.database.influx import h2m_boot_influx_database
from kotori.hydro2motion.network.udp import h2m_boot_udp_adapter
from kotori.hiveeyes.application import hiveeyes_boot
from .version import __VERSION__

__path__ = extend_path(__path__, __name__)

__doc__ = """Kotori node service.

Usage:
  kotori --config=<kotori.ini> [--debug]
  kotori (-h | --help)
  kotori --version

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  --config=<kotori.ini>     Configuration file
  --debug                   Enable debug messages

"""
"""
deprecated:
  #kotori master [--debug]
  #kotori node --master=<> [--debug]
"""
from docopt import docopt

logger = Logger()

def run():

    startLogging(sys.stdout)

    application_string = 'Kotori DAQ version ' + __VERSION__
    logger.info(application_string)

    options = docopt(__doc__, version=application_string)
    print 'options: {}'.format(options)
    debug = options.get('--debug', False)
    print "debug:", debug

    configfile = options['--config']
    config = ConfigParser()
    success = config.read([configfile, os.path.expanduser('~/.kotori.ini')])
    if success:
        logger.info('Read configuration files: {}'.format(success))
        logger.info('config: {}'.format(config))
    else:
        msg = 'Could not read configuration file {}'.format(configfile)
        logger.error(msg)
        raise ValueError(msg)

    # defaults
    websocket_uri = unicode(config.get('wamp', 'listen'))
    http_port_v2 = int(config.get('kotori-daq', 'http_port'))

    # run master and web gui
    if 'master' in options:
        boot_master(websocket_uri, debug)
        boot_web(35000, '', debug)
        #boot_udp_adapter(udp_port, debug)

    # run node and web gui only, using a remote master
    if 'node' in options:
        websocket_uri = options['--master']
        boot_web(35000, websocket_uri, debug)
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
            udp_port = int(config.get('hydro2motion', 'udp_port'))
            http_port_v1 = int(config.get('hydro2motion', 'http_port'))

            boot_web(http_port_v1, websocket_uri, debug=debug)
            h2m_boot_udp_adapter(udp_port, debug=debug)
            h2m_boot_influx_database(config)

        # hiveeyes
        hiveeyes_boot(config, debug=debug)

        # generic daq
        boot_frontend(frontend_port, websocket_uri, debug=debug)


    # now enter the Twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    run()
