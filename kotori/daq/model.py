# -*- coding: utf-8 -*-
# (c) 2023 Andreas Motl, <andreas@getkotori.org>
from enum import Enum


class TimeseriesDatabaseType(Enum):
    CRATEDB = "cratedb"
    INFLUXDB1 = "influxdb"
