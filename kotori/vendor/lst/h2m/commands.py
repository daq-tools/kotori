# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import socket
import logging
from pprint import pprint
from docopt import docopt, DocoptExit
from binascii import unhexlify
from urlparse import urlparse
from kotori.vendor.lst.h2m.util import setup_logging, setup_h2m_structs
from kotori.vendor.lst.message import BinaryMessageAdapter

APP_NAME = 'h2m-message 0.1.0'

messenger = None

logger = logging.getLogger(__name__)

def h2m_message_cmd():
    """
    Usage:
      h2m-message decode <payload> [--debug]
      h2m-message send   <payload> --target=udp://localhost:8888
      h2m-message info   <name>    [--debug]
      h2m-message --version
      h2m-message (-h | --help)

    Options:
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    """
    options = docopt(h2m_message_cmd.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    debug = options.get('--debug')
    target = options.get('--target')

    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # initialize "h2m_structs" library
    global messenger
    messenger = BinaryMessageAdapter(struct_registry=setup_h2m_structs())

    if options.get('decode'):
        payload = options.get('<payload>')

        # decode from 8-bit clean hex format, e.g. ``0x05022a0021``
        payload = decode_payload(payload)

        # decode binary message
        struct = messenger.decode(payload)
        messenger.pprint(struct)

    elif options.get('info'):
        name = options.get('<name>')
        struct_adapter = messenger.struct_registry.get(name)
        struct_adapter.print_schema()

    elif options.get('send'):
        uri = urlparse(target)
        if uri.scheme == 'udp':

            payload_ascii = options.get('<payload>')

            # decode from 8-bit clean hex format, e.g. ``0x05022a0021``
            payload = decode_payload(payload_ascii)

            # decode binary message
            struct = messenger.decode(payload)
            #messenger.pprint(struct)

            # send message via UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.sendto(struct._dump_(), (uri.hostname, uri.port))
            logger.info('Message "{}" sent to "{}"'.format(payload_ascii, target))

        else:
            raise DocoptExit('Can not send message to target "{}", unknown protocol "{}"'.format(target, uri.scheme))


def decode_payload(payload):
    # decode data payload from 8-bit clean hex format, e.g. ``0x05022a0021``
    logger.debug('Decoding payload "{}"'.format(payload))
    if payload.startswith('0x'):
        payload = payload.replace('0x', '')
        payload = unhexlify(payload)
    else:
        raise ValueError('Can not decode "{}"'.format(payload))

    return payload
