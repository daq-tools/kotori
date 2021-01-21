# -*- coding: utf-8 -*-
# (c) 2019-2021 Andreas Motl <andreas@getkotori.org>
from kotori.daq.decoder.airrohr import AirrohrDecoder
from kotori.daq.decoder.json import CompactTimestampedJsonDecoder
from kotori.daq.decoder.tasmota import TasmotaSensorDecoder, TasmotaStateDecoder
from kotori.daq.decoder.schema import MessageType


class DecoderInfo:

    def __init__(self):
        self.message_type = None
        self.decoder = None


class DecoderManager:

    def __init__(self, topology):
        self.topology = topology
        self.info = DecoderInfo()

    def probe(self):

        if 'slot' not in self.topology:
            return False

        # Compact JSON format, with timestamps as keys
        if self.topology.slot.endswith('tc.json'):
            self.info.message_type = MessageType.DATA_CONTAINER
            self.info.decoder = CompactTimestampedJsonDecoder
            return True

        # Airrohr
        if self.topology.slot.endswith('airrohr.json'):
            self.info.message_type = MessageType.DATA_CONTAINER
            self.info.decoder = AirrohrDecoder
            return True

        # Tasmota Sensor
        if self.topology.slot.endswith('SENSOR'):
            self.info.message_type = MessageType.DATA_CONTAINER
            self.info.decoder = TasmotaSensorDecoder
            return True

        # Tasmota State
        if self.topology.slot.endswith('STATE'):
            self.info.message_type = MessageType.DATA_CONTAINER
            self.info.decoder = TasmotaStateDecoder
            return True

        return False
