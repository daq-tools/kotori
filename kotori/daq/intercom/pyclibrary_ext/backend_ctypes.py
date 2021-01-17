# -*- coding: utf-8 -*-
import pyclibrary
import ctypes
from ctypes import Union, Structure

# taken verbatim from pyclibrary.backends.ctypes.CTypesCLibrary._get_struct
# 2015-11-07 improve _fields_ and _defaults_ building

class StructureWithDefaults(Structure):

    def __init__(self, **kwargs):
        """
        Ctypes.Structure with integrated default values.
        https://stackoverflow.com/questions/7946519/default-values-in-a-ctypes-structure/25892189#25892189

        :param kwargs: values different to defaults
        :type kwargs: dict
        """

        # sanity checks
        defaults = type(self)._defaults_
        assert type(defaults) is dict

        # use defaults, but override with keyword arguments, if any
        values = defaults.copy()
        for (key, val) in kwargs.items():
            values[key] = val

        # appropriately initialize ctypes.Structure
        #super().__init__(**values)                     # Python 3 syntax
        return Structure.__init__(self, **values)       # Python 2 syntax

    # http://stackoverflow.com/questions/1825715/how-to-pack-and-unpack-using-ctypes-structure-str/1827666#1827666
    # https://wiki.python.org/moin/ctypes
    def _dump_(self):
        right = ctypes.sizeof(self) - 1
        return buffer(self)[:right]

    def _load_(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)


def _get_struct(self, str_type, str_name):
    if str_name not in self._structs_:

        str_name = self._resolve_struct_alias(str_type, str_name)

        # Pull struct definition
        defn = self._defs_[str_type][str_name]

        # create ctypes class
        defs = defn['members'][:]
        if str_type == 'structs':
            class s(StructureWithDefaults):
                def __repr__(self):
                    return "<ctypes struct '%s'>" % str_name
                def _name_(self):
                    return str_name
        elif str_type == 'unions':
            class s(Union):
                def __repr__(self):
                    return "<ctypes union '%s'>" % str_name
                def _name_(self):
                    return str_name

        # Must register struct here to allow recursive definitions.
        self._structs_[str_name] = s

        if defn['pack'] is not None:
            s._pack_ = defn['pack']

        # Assign names to anonymous members
        members = []
        anon = []
        for i, d in enumerate(defs):
            if d[0] is None:
                c = 0
                while True:
                    name = 'anon_member%d' % c
                    if name not in members:
                        d[0] = name
                        anon.append(name)
                        break
            members.append(d[0])

        s._anonymous_ = anon

        # Handle bit field specifications, ctypes only supports bit fields
        # for integer but I am not sure how to test for it in a nice
        # fashion.

        # compute fields
        _fields = []
        for m in defs:
            if len(m) <= 3:
                # the _third_ part of the member definition tuple contains the default value,
                # which should _not_ get used when defining the bare _field_
                t = (m[0], self._get_type(m[1]))

            elif len(m) == 4:
                # the _fourth_ part of the member definition tuple contains the bit width,
                # which _should_ be used when defining the bare _field_
                t = (m[0], self._get_type(m[1]), m[3])

            _fields.append(t)

        # compute defaults
        # the _third_ slot of the member definition tuple contains the default value
        _defaults = {}
        for m in defs:
            if len(m) >= 3:
                key = m[0]
                value = m[2]
                if value:
                    _defaults[key] = value

        s._fields_ = _fields
        s._defaults_ = _defaults

    return self._structs_[str_name]


def monkeypatch_pyclibrary_ctypes_struct():
    pyclibrary.backends.ctypes.CTypesCLibrary._get_struct = _get_struct
