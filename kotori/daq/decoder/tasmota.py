# -*- coding: utf-8 -*-
# (c) 2019-2021 Andreas Motl <andreas@getkotori.org>
"""
Decode JSON payloads in Tasmota format.

Documentation
=============
- https://getkotori.org/docs/handbook/decoders/tasmota.html

Resources
=========
- https://github.com/arendst/tasmota
- https://github.com/arendst/tasmota/wiki/MQTT
- https://tasmota.github.io/docs/#/MQTT
"""
import json
from collections import OrderedDict
from copy import deepcopy


class TasmotaSensorDecoder:

    @staticmethod
    def decode(payload):
        """
        SonoffSC::

            {
              "Time": "2019-06-02T22:13:07",
              "SonoffSC": {
                "Temperature": 25,
                "Humidity": 15,
                "Light": 20,
                "Noise": 10,
                "AirQuality": 90
              },
              "TempUnit": "C"
            }

        Sonoff DS18B20::

            {
              "Time": "2017-02-16T10:13:52",
              "DS18B20": {
                "Temperature": 20.6
              }
            }

        Wemos Multi::

            {
              "Time": "2017-10-05T22:39:45",
              "DS18x20": {
                "DS1": {
                  "Type": "DS18B20",
                  "Address": "28FF4CBFA41604C4",
                  "Temperature": 25.37
                },
                "DS2": {
                  "Type": "DS18B20",
                  "Address": "28FF1E7FA116035D",
                  "Temperature": 30.44
                },
                "DS3": {
                  "Type": "DS18B20",
                  "Address": "28FF1597A41604CE",
                  "Temperature": 25.81
                }
              },
              "DHT22": {
                "Temperature": 33.2,
                "Humidity": 30
              },
              "TempUnit": "C"
            }

        """

        # Decode from JSON.
        message = json.loads(payload)

        # Decode message format.
        data = OrderedDict()

        # Transfer timestamp field.
        if 'Time' in message:
            data['Time'] = message['Time']

        # Transfer measurement fields.
        path = []
        for key, value in message.items():
            path.append(key)
            if isinstance(value, dict):
                for dkey, dvalue in value.items():
                    path.append(dkey)
                    if isinstance(dvalue, dict):
                        if 'Type' in dvalue:
                            subdata = deepcopy(dvalue)
                            del subdata['Type']
                            del subdata['Address']
                            for dskey, dsvalue in subdata.items():
                                path.append(dskey)
                                effective_key = '.'.join(path)
                                data[effective_key] = dsvalue
                                path.pop()
                    else:
                        effective_key = '.'.join(path)
                        data[effective_key] = dvalue
                    path.pop()

            path.pop()
        return data


class TasmotaStateDecoder:

    @staticmethod
    def decode(payload):
        """
        {
          "Time": "2019-06-02T22:13:07",
          "Uptime": "1T18:10:35",
          "Vcc": 3.182,
          "SleepMode": "Dynamic",
          "Sleep": 50,
          "LoadAvg": 19,
          "Wifi": {
            "AP": 1,
            "SSId": "{redacted}",
            "BSSId": "A0:F3:C1:{redacted}",
            "Channel": 1,
            "RSSI": 100,
            "LinkCount": 1,
            "Downtime": "0T00:00:07"
          }
        }
        """

        # Decode from JSON.
        message = json.loads(payload)

        # Decode message format.
        data = OrderedDict()
        data['Time'] = message.get('Time')
        data['Device.Vcc'] = message.get('Vcc')
        data['Device.Sleep'] = message.get('Sleep')
        data['Device.LoadAvg'] = message.get('LoadAvg')
        data['Device.Wifi.Channel'] = message.get('Wifi', {}).get('Channel')
        data['Device.Wifi.RSSI'] = message.get('Wifi', {}).get('RSSI')
        data['Device.Wifi.LinkCount'] = message.get('Wifi', {}).get('LinkCount')
        return data
