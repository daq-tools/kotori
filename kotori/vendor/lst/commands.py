# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import socket
import logging
from binascii import unhexlify
from urllib.parse import urlparse

from tabulate import tabulate
from collections import OrderedDict
from kotori.util.configuration import read_list

logger = logging.getLogger(__name__)

CONFIG_CHANNEL_PREFIX = 'lst-'


def sanitize_channel_label(label):
    return label.replace(CONFIG_CHANNEL_PREFIX, '')


def compute_channel_label(name):
    return CONFIG_CHANNEL_PREFIX + name


def lst_channels(config):
    channel_labels = read_list(config['lst']['channels'])
    channel_infos = []
    for channel_label in channel_labels:
        channel_settings = config[channel_label]
        channel_info = get_channel_info(channel_label, channel_settings)
        channel_infos.append(channel_info)
    print(tabulate(channel_infos, headers='keys'))


def get_channel_info(channel_label, channel_settings):
    channel = OrderedDict()
    channel['name']         = sanitize_channel_label(channel_label)
    #channel['label']        = channel_label
    channel['udp port']     = channel_settings['udp_port']
    channel['wamp topic']   = channel_settings['wamp_topic']
    channel['header files'] = channel_settings['header_files']
    channel['path']         = os.path.abspath(channel_settings['include_path'])
    return channel


def lst_message(channel, adapter, options):

    target = options.get('--target')
    struct_name = options.get('<name>')
    payload_ascii = options.get('<payload>')

    if options.get('info'):
        print()
        if struct_name:
            try:
                struct_adapter = adapter.struct_registry.get(struct_name)
                struct_adapter.print_schema()
            except KeyError:
                logger.error('Struct "{struct_name}" not found in channel "{channel_name}"'.format(
                    struct_name=struct_name, channel_name=channel.name))
                sys.exit(1)
        else:
            channel_info = get_channel_info(channel.label, channel.settings)
            struct_infos = adapter.struct_registry.get_metadata()

            print('Channel information'); print()
            print(tabulate(list(zip(list(channel_info.keys()), list(channel_info.values())))))
            print(); print()

            print('Struct information in "{}"'.format(channel.settings.header_files)); print()
            print(tabulate(struct_infos, headers='keys'))

    elif options.get('decode'):
        try:
            struct = decode_payload(adapter, payload_ascii)
            adapter.pprint(struct)
        except KeyError as ex:
            message = 'Decoding binary data "{}" to struct failed.'.format(payload_ascii)
            message += ' ' + ex.message
            logger.error(message)
            sys.exit(1)

    elif options.get('transform'):
        struct = decode_payload(adapter, payload_ascii)
        data = adapter.transform(struct)
        adapter.pprint(struct, data=data)

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
