# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas@getkotori.org>
import json
from collections import OrderedDict


class TheThingsStackDecoder:
    """
    Decode JSON payloads in TTS-/TTN-webhook JSON format.
    TTS/TTN means "The Things Stack" / "The Things Network".

    Documentation
    =============
    - https://getkotori.org/docs/handbook/decoders/tts-ttn.html

    References
    ==========
    - https://www.thethingsindustries.com/docs/the-things-stack/concepts/data-formats/#uplink-messages
    - https://www.thethingsindustries.com/docs/integrations/webhooks/
    - https://community.hiveeyes.org/t/more-data-acquisition-payload-formats-for-kotori/1421
    - https://community.hiveeyes.org/t/tts-ttn-daten-an-kotori-weiterleiten/1422/34
    """

    @staticmethod
    def decode(payload: str):

        # Decode from JSON.
        message = json.loads(payload)

        # Use timestamp and decoded payload.
        data = OrderedDict()
        if "received_at" in message:
            data["timestamp"] = message["received_at"]
        data.update(message["uplink_message"]["decoded_payload"])

        # TODO: Add more data / metadata.
        #       This is an implementation from scratch. It can be improved by
        #       cherry-picking more specific decoding routines from `ttnlogger`.
        #       https://github.com/mqtt-tools/ttnlogger

        return data
