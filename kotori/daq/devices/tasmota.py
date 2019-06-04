# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@getkotori.org>
import types
from collections import OrderedDict


class TasmotaDecoder:

    def __init__(self, topology):
        self.topology = topology

    def decode_message(self, message):
        # Fixme: Currently ignores the "Time" field.
        if 'slot' in self.topology and self.topology.slot.endswith('SENSOR'):
            message = self.decode_sensor_message(message)
        if 'slot' in self.topology and self.topology.slot.endswith('STATE'):
            message = self.decode_state_message(message)
        return message

    def decode_sensor_message(self, message):
        """
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

        {
          "Time": "2017-02-16T10:13:52",
          "DS18B20": {
            "Temperature": 20.6
          }
        }

        """
        data = OrderedDict()
        for key, value in message.items():
            if isinstance(value, types.DictionaryType):
                data.update(value)
        return data

    def decode_state_message(self, message):
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
        data = OrderedDict()
        data['Device.Vcc'] = message.get('Vcc')
        data['Device.Sleep'] = message.get('Sleep')
        data['Device.LoadAvg'] = message.get('LoadAvg')
        data['Device.Wifi.Channel'] = message.get('Wifi', {}).get('Channel')
        data['Device.Wifi.RSSI'] = message.get('Wifi', {}).get('RSSI')
        data['Device.Wifi.LinkCount'] = message.get('Wifi', {}).get('LinkCount')
        return data
