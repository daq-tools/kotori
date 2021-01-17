# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import json
from collections import OrderedDict


class AirrohrDecoder:
    """
    Decode JSON payloads in Airrohr format.

    Documentation
    =============
    - https://getkotori.org/docs/handbook/decoders/airrohr.html
    - https://community.hiveeyes.org/t/more-data-acquisition-payload-formats-for-kotori/1421/2

    Example
    =======
    ::

        {
          "esp8266id": 12041741,
          "sensordatavalues": [
            {
              "value_type": "SDS_P1",
              "value": "35.67"
            },
            {
              "value_type": "SDS_P2",
              "value": "17.00"
            },
            {
              "value_type": "BME280_temperature",
              "value": "-2.83"
            },
            {
              "value_type": "BME280_humidity",
              "value": "66.73"
            },
            {
              "value_type": "BME280_pressure",
              "value": "100535.97"
            },
            {
              "value_type": "samples",
              "value": "3016882"
            },
            {
              "value_type": "min_micro",
              "value": "77"
            },
            {
              "value_type": "max_micro",
              "value": "26303"
            },
            {
              "value_type": "signal",
              "value": "-66"
            }
          ],
          "software_version": "NRZ-2018-123B"
        }

    """

    @staticmethod
    def decode(payload):

        # Decode from JSON.
        message = json.loads(payload)

        # Create data dictionary by flattening nested message.
        data = OrderedDict()
        for item in message.get('sensordatavalues', []):
            key = item['value_type']
            value = item['value']
            data[key] = value

        return data
