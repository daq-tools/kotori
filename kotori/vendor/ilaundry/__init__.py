from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

# deprecated docopt definition
"""
  #kotori master [--debug]
  #kotori node --master=<> [--debug]
"""

# legacy bootstrap code from iLaundry
"""
from kotori.io.master.server import boot_master
from kotori.io.node.nodeservice import boot_node

# defaults
if config.has_section('wamp'):
    websocket_uri = unicode(config.get('wamp', 'listen'))

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
    boot_master(websocket_uri, debug=debug)
    boot_web(http_port, websocket_uri, debug=debug)
    boot_frontend(frontend_port, websocket_uri, debug=debug)
    boot_node(websocket_uri, debug=debug)
    boot_udp_adapter(udp_port, debug=debug)
    boot_sql_database(websocket_uri)
    boot_mongo_database(websocket_uri)
    boot_influx_database(websocket_uri)
"""
