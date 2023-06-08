# -*- coding: utf-8 -*-
# (c) 2019-2023 Andreas Motl <andreas@getkotori.org>
# (c) 2019-2023 Matthias Büchner <m.buechner@gmail.com>
import json
from collections import OrderedDict
import typing as t


MessageValueType = t.Dict[str, t.Union[str, int, float, t.Dict[str, t.Any], t.List[t.Dict]]]


class TheThingsStackDecoder:
    """
    Decode JSON payloads in TTS-/TTN-webhook JSON format.
    TTS/TTN means "The Things Stack" / "The Things Network".

    Documentation
    =============
    - https://getkotori.org/docs/integration/tts-ttn.html

    References
    ==========
    - https://www.thethingsindustries.com/docs/the-things-stack/concepts/data-formats/#uplink-messages
    - https://www.thethingsindustries.com/docs/integrations/webhooks/
    - https://www.thethingsnetwork.org/docs/lorawan/architecture/
    - https://www.thethingsnetwork.org/docs/lorawan/message-types/
    - https://community.hiveeyes.org/t/more-data-acquisition-payload-formats-for-kotori/1421
    - https://community.hiveeyes.org/t/tts-ttn-daten-an-kotori-weiterleiten/1422/34
    """

    @classmethod
    def decode(cls, payload: str):

        # Decode from JSON.
        message = json.loads(payload)

        data = OrderedDict()

        # Decode device id, timestamp, and decoded uplink message payload.
        if "end_device_ids" in message:
            data["device_id"] = message["end_device_ids"]["device_id"]
        if "received_at" in message:
            data["timestamp"] = message["received_at"]

        if "uplink_message" in message:
            data.update(cls.decode_uplink_message(message["uplink_message"]))

        return data

    @classmethod
    def decode_uplink_message(cls, uplink_message: MessageValueType):
        """
        Decode a TTN uplink message, i.e. originating from the appliance/device.
        """

        data = OrderedDict()

        # Decode message payload.
        data.update(uplink_message["decoded_payload"])

        # Extract infrastructure data.
        if "settings" in uplink_message:
            data["bw"] = uplink_message["settings"]["data_rate"]["lora"]["bandwidth"] / 1000
            data["sf"] = uplink_message["settings"]["data_rate"]["lora"]["spreading_factor"]
            data["freq"] = float(uplink_message["settings"]["frequency"]) / 1000000.0
        if "f_cnt" in uplink_message:
            data["counter"] = int(uplink_message["f_cnt"])
        if "rx_metadata" in uplink_message:
            data["gtw_count"] = len(uplink_message["rx_metadata"])
            for rx_metadata in uplink_message["rx_metadata"]:
                gateway_id = rx_metadata["gateway_ids"]["gateway_id"]
                data["gw_" + gateway_id + "_rssi"] = rx_metadata["rssi"]
                data["gw_" + gateway_id + "_snr"] = rx_metadata["snr"]

        return data


if __name__ == "__main__":
    """
    About
    =====
    Decode a TTN JSON payload file on the command line.

    Synopsis
    ========
    ::

        python -m kotori.daq.decoder.tts_ttn "test/test_tts_ttn_full.json"
        python -m kotori.daq.decoder.tts_ttn "test/test_tts_ttn_minimal.json"
    """
    import sys

    filepath = sys.argv[1]
    data = TheThingsStackDecoder.decode(open(filepath).read())
    print(json.dumps(data, indent=2))
