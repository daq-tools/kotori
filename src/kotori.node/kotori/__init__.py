# -*- coding: utf-8 -*-
# (c) 2014-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
from pkgutil import extend_path
from kotori.node.database.influx import boot_influx_database
from kotori.node.database.mongo import boot_mongo_database
from twisted.internet import reactor
from twisted.python import log
from kotori.master.server import boot_master
from kotori.node.nodeservice import boot_node
from kotori.web.server import boot_web
from kotori.node.udp import boot_udp_adapter
from kotori.node.database.sql import boot_sql_database

__path__ = extend_path(__path__, __name__)


__doc__ = """Kotori node service.

Usage:
  kotori [--debug]
  kotori master [--debug]
  kotori node --master=<> [--debug]
  kotori (-h | --help)
  kotori --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --debug       Enable debug messages

"""
from docopt import docopt


"""
#kotori ship <name> move <x> <y> [--speed=<kn>]
#kotori ship shoot <x> <y>
#kotori mine (set|remove) <x> <y> [--moored | --drifting]
"""

def run():

    log.startLogging(sys.stdout)

    arguments = docopt(__doc__, version='Kotori node service')
    #print arguments
    debug = arguments.get('--debug', False)
    print "debug:", debug

    # defaults
    websocket_uri = u'ws://0.0.0.0:9000/ws'
    http_port = 35000
    udp_port = 7777

    # run master and web gui
    if arguments['master']:
        boot_master(websocket_uri, debug)
        boot_web(http_port, '', debug)
        boot_udp_adapter(udp_port, debug)

    # run node and web gui only, using a remote master
    elif arguments['node']:
        websocket_uri = arguments['--master']
        boot_web(http_port, websocket_uri, debug)
        boot_node(websocket_uri, debug)
        boot_udp_adapter(udp_port, debug)

    # run master, node and web gui
    else:
        boot_master(websocket_uri, debug=debug)
        boot_web(http_port, websocket_uri, debug=debug)
        boot_node(websocket_uri, debug=debug)
        boot_udp_adapter(udp_port, debug=debug)
        boot_sql_database(websocket_uri)
        boot_mongo_database(websocket_uri)
        boot_influx_database(websocket_uri)

    # now enter the Twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    run()
