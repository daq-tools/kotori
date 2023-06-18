# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas@getkotori.org>
from twisted.logger import Logger
from kotori.io.protocol.util import compute_daterange, is_number

log = Logger()


class QueryTransformer:

    @classmethod
    def transform(cls, data):
        """
        Compute InfluxDB query expression from data in transformation dictionary.
        Also compute date range from query parameters "from" and "to".
        """

        from pyinfluxql import Query
        from pyinfluxql.functions import Mean

        measurement = data.measurement

        # Vanilla QL (v1)
        #expression = 'SELECT * FROM {measurement}'.format(measurement=measurement)

        # PyInfluxQL (v2)
        # https://github.com/jjmalina/pyinfluxql

        # Labs
        #time_begin = arrow.utcnow() - arrow.Arrow(hour=1)
        #expression = Query('*').from_(measurement).where(time__gt=datetime.utcnow() - timedelta(hours=1))
        #expression = Query(Mean('*')).from_(measurement).where(time__gt=datetime.now() - timedelta(1)).group_by(time=timedelta(hours=1))

        # Fix up "measurement" if starting with numeric value
        # TODO: Fix should go to pyinfluxql
        if is_number(measurement[0]):
            measurement = '"{measurement}"'.format(measurement=measurement)

        # TODO: Use ".date_range" API method
        time_begin, time_end = compute_daterange(data.get('from'), data.get('to'))

        tags = {}
        #tags = InfluxDBAdapter.get_tags(data)

        expression = Query('*').from_(measurement).where(time__gte=time_begin, time__lte=time_end, **tags)

        result = {
            'expression': str(expression),
            'time_begin': time_begin,
            'time_end':   time_end,
        }

        return result
