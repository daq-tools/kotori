# -*- coding: utf-8 -*-
# (c) 2014-2021 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import time
import random
import socket
from twisted.python import log


# derived from https://twistedmatrix.com/documents/15.0.0/core/howto/udp.html
def run_udp_client():
    log.startLogging(sys.stdout)

    #data = 'UDP hello'
    #data = '5;3;'
    try:
        data = sys.argv[1]
    except IndexError:
        data = ''

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.sendto(data, ('127.0.0.1', 7777))


def generate_packet():
    packet_tpl = "24000;{};{};{};{};{};{};{};{};{};0;0;0;0;0;1;0;12;0;0;0;-18;0;4011;417633984;85402624;472851424;0;12242;43;42;0;0"
    values = []
    for i in range(20):
        value = random.randint(0, 99999)
        values.append(value)
    #print values
    packet = packet_tpl.format(*values)
    return packet


def run_udp_fuzzer():
    log.startLogging(sys.stdout)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while True:
        data = generate_packet()
        print('packet:', data)

        sock.sendto(data, ('127.0.0.1', 7777))
        time.sleep(0.25)
