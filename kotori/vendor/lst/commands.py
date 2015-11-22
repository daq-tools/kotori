# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import socket
import logging
from binascii import unhexlify
from urlparse import urlparse
from pprint import pprint

logger = logging.getLogger(__name__)

def lst_message(adapter, options):

    target = options.get('--target')
    payload_ascii = options.get('<payload>')

    if options.get('decode'):
        struct = decode_payload(adapter, payload_ascii)
        adapter.pprint(struct)

    elif options.get('transform'):
        struct = decode_payload(adapter, payload_ascii)
        data = adapter.transform(struct)
        adapter.pprint(struct, data=data)

    elif options.get('info'):
        name = options.get('<name>')
        struct_adapter = adapter.struct_registry.get(name)
        struct_adapter.print_schema()

    elif options.get('send'):
        uri = urlparse(target)
        if uri.scheme == 'udp':

            struct = decode_payload(adapter, payload_ascii)
            #messenger.pprint(struct)

            # send message via UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.sendto(struct._dump_(), (uri.hostname, uri.port))
            logger.info('Message "{}" sent to "{}"'.format(payload_ascii, target))

        else:
            raise ValueError('Can not send message to target "{}", unknown protocol "{}"'.format(target, uri.scheme))


def read_payload(payload):
    # decode data payload from 8-bit clean hex format, e.g. ``0x05022a0021``
    logger.debug('Decoding payload "{}"'.format(payload))
    if payload.startswith('0x'):
        payload = payload.replace('0x', '')
        payload = unhexlify(payload)
    else:
        raise ValueError('Can not decode "{}"'.format(payload))

    return payload


def decode_payload(adapter, payload_ascii):

    # decode from 8-bit clean hex format, e.g. ``0x05022a0021``
    payload = read_payload(payload_ascii)

    # decode binary message
    struct = adapter.decode(payload)

    return struct


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-25s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)