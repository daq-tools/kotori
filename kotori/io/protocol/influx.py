# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl <andreas.motl@elmyra.de>
import types
import arrow
import pandas
import collections
from pprint import pprint
from arrow.parser import DateTimeParser
from datetime import datetime, timedelta
from pyinfluxql import Query
from pyinfluxql.functions import Mean
from twisted.logger import Logger
from kotori.daq.storage.influx import InfluxDBAdapter
from kotori.io.protocol.util import is_number
from kotori.util import tdelta

log = Logger()

class QueryTransformer(object):

    @classmethod
    def transform(cls, data):
        """
        Compute InfluxDB query expression from data in transformation dictionary.
        Also compute date range from query parameters "from" and "to".
        """

        series = data.series

        # Vanilla QL (v1)
        #expression = 'SELECT * FROM {series}'.format(series=series)

        # PyInfluxQL (v2)
        # https://github.com/jjmalina/pyinfluxql

        # Labs
        #time_begin = arrow.utcnow() - arrow.Arrow(hour=1)
        #expression = Query('*').from_(series).where(time__gt=datetime.utcnow() - timedelta(hours=1))
        #expression = Query(Mean('*')).from_(series).where(time__gt=datetime.now() - timedelta(1)).group_by(time=timedelta(hours=1))

        # Fix up "series" if starting with numeric value
        # TODO: Fix should go to pyinfluxql
        if is_number(series[0]):
            series = '"{series}"'.format(series=series)

        time_begin, time_end = compute_daterange(data.get('from'), data.get('to'))

        # TODO: Use ".date_range" API method
        expression = Query('*').from_(series).where(time__gte=time_begin, time__lte=time_end)

        result = {
            'expression': str(expression),
            'time_begin': time_begin,
            'time_end':   time_end,
        }

        return result


class DataFrameQuery(object):
    """
    Query InfluxDB, massage result and return as DataFrame.
    """

    def __init__(self, settings=None, bucket=None):
        self.settings = settings
        self.bucket = bucket
        self.request = bucket.request

    def query(self):

        bucket = self.bucket

        # Get an InfluxDB adapter object
        # TODO: Pool these, keyed by database.
        influx = InfluxDBAdapter(
            settings = self.settings.influxdb,
            database = bucket.tdata.database)

        # Get query expression from transformation dictionary
        expression = bucket.tdata.expression

        log.info('InfluxDB expression: {expression}', expression=expression)

        # Run database query
        result = influx.influx.query(expression)

        # Massage result format
        entries = list(flatten(result))

        # Stop when having no results
        if not entries:
            return

        # Bring column names in order, "time" should be the first column
        columns = entries[0].keys()
        if 'time' in columns:
            columns.remove('time')
            columns.insert(0, 'time')

        # Make pandas DataFrame from database results
        df = pandas.DataFrame(entries, columns=columns)

        # Convert "time" column to datetime format
        df['time'] = pandas.to_datetime(df['time'])

        return df


def get_timedelta(expression):

    # TODO: Use pandas' Timedelta. Timedelta('1m2s')
    # http://pandas.pydata.org/pandas-docs/stable/timedeltas.html

    # FIXME: Sanitize expression
    code = expression
    delta_raw = code.replace('now-', '')
    if code != delta_raw:
        code = code.replace(delta_raw, 'delta')

    # "code" should now be "now-delta"
    #print 'code:', code

    now = datetime.utcnow()
    delta = tdelta(delta_raw)

    # FIXME: This is nasty
    try:
        td = eval(code)
    except:
        raise ValueError('Unknown expression: {expression}'.format(expression=expression))

    return td


def flatten(l):
    """
    Munge InfluxDB results.

    See also: https://stackoverflow.com/questions/21461140/flatten-an-irregular-list-of-lists-in-python-respecting-pandas-dataframes
    """
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (basestring, pandas.DataFrame, types.DictionaryType)):
            for sub in flatten(el):
                yield sub
        else:
            yield el


def compute_daterange(raw_begin, raw_end):

    # Defaults
    raw_begin = raw_begin or 'now-10d'
    raw_end   = raw_end   or 'now'

    # Parse dates, absolute or relative
    time_begin = grok_datetime(raw_begin)
    time_end   = grok_datetime(raw_end)

    # If end of date range is supplied as date without time ('YYYY-MM-DD' or 'YYYYMMDD'),
    # add appropriate offset to mean "end of day" (DWIM).
    if 8 <= len(raw_end) <= 10:
        offset_endofday = tdelta('23h59m59s') + timedelta(microseconds = 999999)
        time_end += offset_endofday

    return time_begin, time_end

def grok_datetime(dstring):
    more_formats = ['YYYYMMDDTHHmmss', 'YYYYMMDDTHHmmssZ']
    parser = DateTimeParser()
    parser.SEPARATORS += ['']

    # Try to parse datetime string in regular ISO 8601 format
    try:
        return parser.parse_iso(dstring)

    # Fall back to parse datetime string in additional convenience formats
    except arrow.parser.ParserError as ex:
        for format in more_formats:
            try:
                return parser.parse(dstring, format)
            except arrow.parser.ParserError as ex:
                pass

    # Fall back to attempt to parse as relative datetime expression, e.g. "now-10m"
    return get_timedelta(dstring)

