# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import logging
from pprint import pprint
from binascii import unhexlify, hexlify
from kotori.util.common import setup_logging
from kotori.vendor.lst.h2m.util import setup_h2m_structs
from kotori.daq.intercom.c import LibraryAdapter, StructRegistry, StructRegistryByID

logger = logging.getLogger(__name__)


def getting_started(sr):
# create a "cap_r" struct and print attributes with default values
    print('-' * 42)
    p = sr.create('struct_cap_r')
    print('thing: ', p)
    print('length:', p.length)
    print('ID:    ', p.ID)

    # create a "cap_r" struct overriding default values and print the relevant attributes
    print('-' * 42)
    p = sr.create('struct_cap_r', ID=88)
    print('thing: ', p)
    print('length:', p.length)
    print('ID:    ', p.ID)


    # get lowlevel pyclibrary ctypes backend handle of "struct_program"
    print('-' * 42)
    print('struct_program (schema):')
    struct_program = sr.get('struct_program')
    pprint(struct_program)
    csp = struct_program.obj() #(abc=9)
    print('thing:      ', csp)
    print('length:     ', csp.length)
    print('ID:         ', csp.ID)
    print('send_ser:   ', csp.send_ser)
    print('cfg_loaded: ', csp.cfg_loaded)

    print('-' * 42)
    print('struct_program (instance):')
    print('thing:      ', csp())
    print('length:     ', csp().length)
    print('ID:         ', csp().ID)


    # get lowlevel pyclibrary ctypes backend handle of "struct_cap_r"
    print('-' * 42)
    c = sr.get('struct_cap_r').obj()
    print('thing: ', c)
    print('length:', c.length)
    print('ID:    ', c.ID)

    print('FIELDS:')
    pprint(c._fields_)
    print('DEFAULTS:')
    pprint(c._defaults_)


def dump_full(sr):

    """
    s_program = sr.get('struct_program')
    print s_program
    ast = s_program.ast()
    print dir(ast.members)
    print ast.members
    """

    program = sr.create('struct_program')
    sr.pprint(program)

    gps_w = sr.create('struct_gps_w')
    sr.pprint(gps_w)


def fill_and_dump(sr):

    program = sr.create('struct_program')
    d = sr.to_dict(program)
    pprint(list(d.items()))
    print('dump-1:', hexlify(program._dump_()))

    remote = unhexlify('0d99000000000000000000000000')
    program._load_(remote)
    print('dump-2:', hexlify(program._dump_()))

    program.ID = 88
    print('dump-3:', hexlify(program._dump_()))
    d = sr.to_dict(program)

    # https://stackoverflow.com/questions/4301069/any-way-to-properly-pretty-print-ordered-dictionaries-in-python
    # https://bugs.python.org/issue10592
    # https://bugs.python.org/issue7434
    # https://stackoverflow.com/questions/21420243/pretty-printing-ordereddicts-using-pprint
    pprint(dict(list(d.items())))


def pretend_receive_and_process(sr):

    # let's pretend this is the message received, having ID=2
    payload = unhexlify('05022a0021')

    # decode struct ID from binary data
    message_id = ord(payload[1])

    # look up proper StructAdapter object
    # it should be "struct_cap_r", registered with ID=2
    struct_cap_r = sr.get_by_id(message_id)

    # create instance of struct
    cap_r = struct_cap_r.create()

    # load binary message payload into struct
    cap_r._load_(payload)

    # pretty-print struct content
    #sr.pprint(cap_r)
    #print '=' * 21
    sr.pprint(cap_r, format='tabulate-plain')


def display_schema(sr):
    struct_h2o_w = sr.get('struct_h2o_w')
    struct_h2o_w.print_schema()


def main():

    setup_logging(logging.INFO)

    # initialize "h2m_structs" library
    sr = setup_h2m_structs()

    # call some examples
    #getting_started(sr)
    #dump_full(sr)
    #fill_and_dump(sr)
    #pretend_receive_and_process(sr)
    display_schema(sr)


if __name__ == '__main__':
    main()
