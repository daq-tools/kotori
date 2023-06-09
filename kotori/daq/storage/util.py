# -*- coding: utf-8 -*-
# (c) 2015-2023 Andreas Motl <andreas@getkotori.org>
import math

from kotori.io.protocol.util import convert_floats, is_number, parse_timestamp


def format_chunk(meta, data):
    """
    Format for InfluxDB >= 0.9::
    {
        "measurement": "hiveeyes_100",
        "tags": {
            "host": "server01",
            "region": "europe"
        },
        "time": "2015-10-17T19:30:00Z",
        "fields": {
            "value": 0.42
        }
    }
    """

    assert isinstance(data, dict), 'Data payload is not a dictionary'

    chunk = {
        "measurement": meta['measurement'],
        "tags": {},
    }

    """
    if "gateway" in meta:
        chunk["tags"]["gateway"] = meta["gateway"]

    if "node" in meta:
        chunk["tags"]["node"]    = meta["node"]
    """

    # TODO: Refactor to some knowledgebase component.
    time_field_candidates = [
        'time',  # Vanilla
        'datetime',  # Vanilla
        'Time',  # Tasmota
        'dateTime',  # WeeWX
        'timestamp',  # Contrib
    ]

    # Extract timestamp field from data
    chunk['time_precision'] = 'n'
    # FIXME: Unify with ``kotori.io.protocol.http.data_acquisition()``.
    for time_field in time_field_candidates:
        if time_field in data:

            # WeeWX. TODO: Move to specific vendor configuration.
            # Disabled in favor of precision detection heuristic.
            # if time_field == 'dateTime':
            #    chunk['time_precision'] = 's'

            # Process timestamp field.
            if data[time_field]:

                # Decode timestamp.
                chunk['time'] = data[time_field]
                if is_number(chunk['time']):
                    chunk['time'] = float(chunk['time'])

                # Remove timestamp from data payload.
                del data[time_field]

                # If we found a timestamp field already,
                # don't look out for more.
                break

    # Extract geohash from data. Finally, thanks Rich!
    # TODO: Also precompute geohash with 3-4 different zoomlevels and add them as tags
    if "geohash" in data:
        chunk["tags"]["geohash"] = data["geohash"]
        del data['geohash']

    # Extract more information specific to luftdaten.info
    for field in ['location', 'location_id', 'location_name', 'sensor_id', 'sensor_type']:
        if field in data:
            chunk["tags"][field] = data[field]
            del data[field]

    # TODO: Maybe do this at data acquisition / transformation time, not here.
    if 'time' in chunk:
        timestamp = chunk['time'] = parse_timestamp(chunk['time'])

        # Heuristically compute timestamp precision
        if isinstance(timestamp, (int, float)):
            if timestamp >= 1e17 or timestamp <= -1e17:
                time_precision = 'n'
            elif timestamp >= 1e14 or timestamp <= -1e14:
                time_precision = 'u'
            elif timestamp >= 1e11 or timestamp <= -1e11:
                time_precision = 'ms'

            # TODO: Is this a reasonable default?
            else:
                time_precision = 's'

                # Support fractional epoch timestamps like `1637431069.6585083`.
                if isinstance(timestamp, float):
                    fractional, whole = math.modf(timestamp)
                    fracdigits = len(str(fractional)) - 2
                    if fracdigits > 0:
                        if fracdigits <= 3:
                            exponent = 3
                            time_precision = "ms"
                        elif fracdigits <= 6:
                            exponent = 6
                            time_precision = "u"
                        else:
                            exponent = 9
                            time_precision = "n"
                        timestamp = timestamp * (10 ** exponent)

            chunk['time'] = int(timestamp)
            chunk['time_precision'] = time_precision

        """
        # FIXME: Breaks CSV data acquisition. Why?
        if isinstance(chunk['time'], datetime.datetime):
            if chunk['time'].microsecond == 0:
                chunk['time_precision'] = 's'
        """

    # Make sure numeric data in `fields` is in float format.
    """
    Prevent errors like
    ERROR: InfluxDBClientError: 400:
                   write failed: field type conflict:
                   input field "pitch" on measurement "01_position" is type float64, already exists as type integer
    """
    convert_floats(data)

    assert data, 'Data payload is empty'

    chunk["fields"] = data

    return chunk
