# -*- coding: utf-8 -*-
# (c) 2016-2023 Andreas Motl <andreas@getkotori.org>
import collections.abc
from twisted.logger import Logger

log = Logger()


class DataFrameQuery:
    """
    Query database, reshape result, and return as pandas DataFrame.
    """

    def __init__(self, settings=None, bucket=None):
        self.settings = settings
        self.bucket = bucket
        self.request = bucket.request

    def query(self):

        bucket = self.bucket

        log.info("Creating database adapter")

        # Get a database adapter object.
        # TODO: Support multiple databases at the same time.
        # TODO: Pool adapter instances, keyed by database.
        if "influxdb" in self.settings:
            from kotori.daq.storage.influx import InfluxDBAdapter
            database = InfluxDBAdapter(
                settings=self.settings.influxdb,
                database=bucket.tdata.database,
            )
        else:
            log.warn("No time-series database configured")
            return

        # Get query expression from transformation dictionary.
        expression = bucket.tdata.expression
        log.info('Query expression: {expression}', expression=expression)

        # Run database query.
        result = database.query(expression, tdata=bucket.tdata)

        # Bring results into records format.
        # [{'time': '2020-03-10T03:29:42Z', 'humidity': 51.8, 'temperature': 25.26}]
        records = list(flatten(result))

        # Stop when having no results.
        if not records:
            return

        # Bring column names in order, `time` should be the first column.
        columns = list(records[0].keys())
        if 'time' in columns and columns.index('time') != 0:
            columns.remove('time')
            columns.insert(0, 'time')

        # Produce pandas DataFrame from database results.
        import pandas
        df = pandas.DataFrame(records, columns=columns)

        # Convert `time` column to a pandas datetime object.
        df['time'] = pandas.to_datetime(df['time'])

        return df


def flatten(l):
    """
    Flatten irregular/nested results.

    See also: https://stackoverflow.com/questions/21461140/flatten-an-irregular-list-of-lists-in-python-respecting-pandas-dataframes
    """
    import pandas
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, pandas.DataFrame, dict)):
            for sub in flatten(el):
                yield sub
        else:
            yield el
