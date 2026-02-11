# -*- coding: utf-8 -*-
# (c) 2021 Andreas Motl <andreas@getkotori.org>
import json


class CompactTimestampedJsonDecoder:
    """
    Decode JSON payloads in compact format, with timestamps as keys.

    Documentation
    =============
    - https://getkotori.org/docs/handbook/decoders/json.html (not yet)
    - https://github.com/daq-tools/kotori/issues/39

    Example
    =======
    ::

        {
          "1611082554": {
            "temperature": 21.42,
            "humidity": 41.55
          },
          "1611082568": {
            "temperature": 42.84,
            "humidity": 83.1
          }
        }

    """

    @staticmethod
    def decode(payload):

        # Decode from JSON.
        message = json.loads(payload)

        # Create list of data dictionaries.
        data = []
        for timestamp, item in message.items():
            item["time"] = timestamp
            data.append(item)

        return data
