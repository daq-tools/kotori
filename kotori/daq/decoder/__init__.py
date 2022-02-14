# -*- coding: utf-8 -*-
# (c) 2019-2021 Andreas Motl <andreas@getkotori.org>
from kotori.daq.decoder.airrohr import AirrohrDecoder
from kotori.daq.decoder.tasmota import TasmotaSensorDecoder, TasmotaStateDecoder
from kotori.daq.decoder.schema import MessageType
from kotori.daq.decoder.tts_ttn import TheThingsStackDecoder


class DecoderInfo:

    def __init__(self):
        self.message_type = None
        self.decoder = None


class DecoderManager:

    def __init__(self, topology):
        self.topology = topology
        self.info = DecoderInfo()

    def probe(self, payload: str = None):

        if 'slot' not in self.topology:
            return False

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

        # TTS/TTN: The Things Stack / The Things Network
        print("self.topology:", self.topology)
        if self.topology.slot.endswith('data.json') \
                and payload is not None \
                and "uplink_message" in payload \
                and "decoded_payload" in payload:
            self.info.message_type = MessageType.DATA_CONTAINER
            self.info.decoder = TheThingsStackDecoder
            return True

        return False
