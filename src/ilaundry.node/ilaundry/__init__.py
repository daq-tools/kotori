import sys
from pkgutil import extend_path
from ilaundry.master.server import boot_master
from ilaundry.node.nodeservice import boot_slave
from twisted.internet import reactor
from twisted.python import log

__path__ = extend_path(__path__, __name__)


def run():

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False


    websocket_uri = 'ws://localhost:9000'
    http_port = 35000

    boot_master(websocket_uri, http_port, debug)
    boot_slave(websocket_uri, debug)

    reactor.run()


if __name__ == '__main__':
    run()
