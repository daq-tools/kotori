# -*- coding: utf-8 -*-
# (c) 2023 Andreas Motl <andreas@getkotori.org>
from twisted.logger import Logger

from kotori.io.protocol.util import compute_daterange

log = Logger()


class QueryTransformer:

    @classmethod
    def transform(cls, data):
        """
        Compute CrateDB query expression from data in transformation dictionary.
        Also compute date range from query parameters "from" and "to".
        """

        log.info(f"Querying database: {data}")

        # The PyInfluxQL query generator is versatile enough to be used for all SQL databases.
        from pyinfluxql import Query

        # TODO: Use ".date_range" API method
        time_begin, time_end = compute_daterange(data.get('from'), data.get('to'))

        # TODO: Add querying by tags.
        tags = {}
        # tags = CrateDBAdapter.get_tags(data)

        table = f"{data.database}.{data.measurement}"
        expression = Query('*').from_(table).where(time__gte=time_begin, time__lte=time_end, **tags)

        result = {
            'expression': str(expression),
            'time_begin': time_begin,
            'time_end':   time_end,
        }

        return result
