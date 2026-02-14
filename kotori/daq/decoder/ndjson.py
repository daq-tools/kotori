# -*- coding: utf-8 -*-
# (c) 2023 Andreas Motl <andreas@getkotori.org>


class NdJsonDecoder:
    """
    Decode NDJSON payloads. NDJSON is a newline-delimited JSON format.
    It is suitable for submitting multiple JSON records in bulk, or for
    streaming them.

    NDJSON has been called LDJSON, and is also known as JSON Lines, see
    also JSON streaming.

    - http://ndjson.org/
    - https://jsonlines.org/
    - https://en.wikipedia.org/wiki/JSON_streaming

    Documentation
    =============
    - https://getkotori.org/docs/handbook/decoders/ndjson.html (not yet)

    Example
    =======
    ::

        {"temperature":21.42,"humidity":41.55}
        {"temperature":42.84,"humidity":83.1}

    """

    @staticmethod
    def decode(payload):

        # Decode from NDJSON, using pandas.
        import io
        import pandas as pd
        df = pd.read_json(io.StringIO(payload), lines=True)

        # Transform to records again.
        data = df.to_dict(orient="records")
        return data
