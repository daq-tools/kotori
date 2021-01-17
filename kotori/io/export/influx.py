# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas@getkotori.org>
import collections
from twisted.logger import Logger
from kotori.daq.storage.influx import InfluxDBAdapter

log = Logger()


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
            settings=self.settings.influxdb,
            database=bucket.tdata.database)

        # Get query expression from transformation dictionary
        expression = bucket.tdata.expression

        log.info('InfluxDB expression: {expression}', expression=expression)

        # Run database query
        result = influx.influx_client.query(expression)

        # Massage result format
        entries = list(flatten(result))

        # Stop when having no results
        if not entries:
            return

        # Bring column names in order, "time" should be the first column
        columns = list(entries[0].keys())
        if 'time' in columns:
            columns.remove('time')
            columns.insert(0, 'time')

        # Make pandas DataFrame from database results
        import pandas
        df = pandas.DataFrame(entries, columns=columns)

        # Convert "time" column to datetime format
        df['time'] = pandas.to_datetime(df['time'])

        return df


def flatten(l):
    """
    Munge InfluxDB results.

    See also: https://stackoverflow.com/questions/21461140/flatten-an-irregular-list-of-lists-in-python-respecting-pandas-dataframes
    """
    import pandas
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, pandas.DataFrame, dict)):
            for sub in flatten(el):
                yield sub
        else:
            yield el
