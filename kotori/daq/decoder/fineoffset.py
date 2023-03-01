# -*- coding: utf-8 -*-
# (c) 2023 Andreas Motl <andreas@getkotori.org>
import typing as t


class FineOffsetDecoder:
    """
    Decode data format submitted by Fine Offset (FOSHK) weather stations, using the
    excellent `ecowitt2mqtt` machinery [1].

    By wrapping it into a Kotori decoder, it will simplify operation and maintenance.
    Effectively, there are fewer moving parts involved, yet all features can be leveraged:

    - anonymization of data
    - convenience of unit conversion
    - additional calculated values
    - integrated test coverage
    - no installation overhead

    Despite the name of the library, `ecowitt2mqtt` [2] supports any weather
    station/gateway that is produced by Shenzhen Fine Offset Electronics Co., Ltd. [3]
    aka. Fine Offset aka. OFFSET. This includes brands that white-label Fine Offset
    equipment, such as:

    - Ambient Weather (U.S.)
    - Ecowitt (China, Hong Kong)
    - Froggit (Germany)

    ...and many others. For more information on how these brands relate to one another,
    see the forum post at [4].

    Although there are some small differences between how these various branded devices
    are configured, `ecowitt2mqtt` endeavors to incorporate them all with minimal effort
    on the user's part [5].

    `ecowitt2mqtt` currently supports the following input data formats [6]:

    - `ambient_weather`
    - `ecowitt`

    [1] https://community.hiveeyes.org/t/more-data-acquisition-payload-formats-for-kotori/1421/17
    [2] https://github.com/bachya/ecowitt2mqtt
    [3] https://www.foshk.com/
    [4] https://www.wxforum.net/index.php?topic=40730.0
    [5] https://github.com/bachya/ecowitt2mqtt/tree/dev#supported-brands
    [6] https://github.com/bachya/ecowitt2mqtt/tree/dev#input-data-formats

    Example data
    ============

    This is an input data sample provided by an Ecowitt weather station, then
    converted to the "metric" unit system and with additional computed values
    by `ecowitt2mqtt`, displayed in the "Output" section.

    Input
    -----
    ::

        {
            "PASSKEY": "B950C...[obliterated]",
            "stationtype": "EasyWeatherPro_V5.0.6",
            "runtime": "456128",
            "dateutc": "2023-02-20 16:02:19",
            "tempinf": "69.8",
            "humidityin": "47",
            "baromrelin": "29.713",
            "baromabsin": "29.713",
            "tempf": "48.4",
            "humidity": "80",
            "winddir": "108",
            "windspeedmph": "1.12",
            "windgustmph": "4.92",
            "maxdailygust": "12.97",
            "solarradiation": "1.89",
            "uv": "0",
            "rainratein": "0.000",
            "eventrainin": "0.000",
            "hourlyrainin": "0.000",
            "dailyrainin": "0.028",
            "weeklyrainin": "0.098",
            "monthlyrainin": "0.909",
            "yearlyrainin": "0.909",
            "temp1f": "45.0",
            "humidity1": "90",
            "soilmoisture1": "46",
            "soilmoisture2": "53",
            "tf_ch1": "41.9",
            "rrain_piezo": "0.000",
            "erain_piezo": "0.000",
            "hrain_piezo": "0.000",
            "drain_piezo": "0.028",
            "wrain_piezo": "0.043",
            "mrain_piezo": "0.492",
            "yrain_piezo": "0.492",
            "wh65batt": "0",
            "wh25batt": "0",
            "batt1": "0",
            "soilbatt1": "1.6",
            "soilbatt2": "1.6",
            "tf_batt1": "1.60",
            "wh90batt": "3.04",
            "freq": "868M",
            "model": "HP1000SE-PRO_Pro_V1.8.5",
        }

    Output
    ------
    ::

        {
          "runtime": 456128.0,
          "tempin": 20.999999999999996,
          "humidityin": 47.0,
          "baromrel": 1006.1976567045213,
          "baromabs": 1006.1976567045213,
          "temp": 9.11111111111111,
          "humidity": 80.0,
          "winddir": 108.0,
          "windspeed": 1.8024652800000003,
          "windgust": 7.91797248,
          "maxdailygust": 20.873191679999998,
          "solarradiation": 1.89,
          "uv": 0.0,
          "rainrate": 0.0,
          "eventrain": 0.0,
          "hourlyrain": 0.0,
          "dailyrain": 0.7112,
          "weeklyrain": 2.4892000000000003,
          "monthlyrain": 23.0886,
          "yearlyrain": 23.0886,
          "temp1": 7.222222222222222,
          "humidity1": 90.0,
          "soilmoisture1": 46.0,
          "soilmoisture2": 53.0,
          "tf_ch1": 5.499999999999999,
          "rrain_piezo": 0.0,
          "erain_piezo": 0.0,
          "hrain_piezo": 0.0,
          "drain_piezo": 0.7112,
          "wrain_piezo": 1.0921999999999998,
          "mrain_piezo": 12.4968,
          "yrain_piezo": 12.4968,
          "wh65batt": "OFF",
          "wh25batt": "OFF",
          "batt1": "OFF",
          "soilbatt1": 1.6,
          "soilbatt2": 1.6,
          "tf_batt1": 1.6,
          "wh90batt": 3.04,
          "beaufortscale": 1,
          "dewpoint": 5.846942096976985,
          "feelslike": 9.11111111111111,
          "frostpoint": 4.706401162443284,
          "frostrisk": "No risk",
          "heatindex": 8.166666666666668,
          "humidex": 9,
          "humidex_perception": "Comfortable",
          "humidityabs": 7.101409765339333,
          "humidityabsin": 7.101409765339333,
          "relative_strain_index": null,
          "relative_strain_index_perception": null,
          "safe_exposure_time_skin_type_1": null,
          "safe_exposure_time_skin_type_2": null,
          "safe_exposure_time_skin_type_3": null,
          "safe_exposure_time_skin_type_4": null,
          "safe_exposure_time_skin_type_5": null,
          "safe_exposure_time_skin_type_6": null,
          "simmerindex": null,
          "simmerzone": null,
          "solarradiation_perceived": 47.57669425765605,
          "thermalperception": "Dry",
          "windchill": null
        }

    """

    @staticmethod
    def detect(data: t.Dict[str, str]) -> bool:
        """
        Determine whether the data payload is submitted by a Fine Offset device.

        TODO: Maybe leverage field names in `ecowitt2mqtt.data.DEFAULT_KEYS_TO_IGNORE`?
        """
        return "PASSKEY" in data and "stationtype" in data and "model" in data

    @staticmethod
    def decode(data: t.Dict[str, str]) -> t.Dict[str, t.Any]:
        """
        Decode data payload submitted by a Fine Offset device, using `ecowitt2mqtt`.
        """

        # This variant is compatible with modern releases like `ecowitt2mqtt-2023.2.1`.
        try:
            from ecowitt2mqtt.config import Config
            from ecowitt2mqtt.data import ProcessedData

            config = Config(
                {
                    # Both configuration variables are currently *required* by `ecowitt2mqtt`.
                    # Fortunately, `mqtt_broker` can be left empty.
                    # TODO: Can this be improved if upstream would accept a corresponding patch?
                    "hass_discovery": True,
                    "mqtt_broker": "",
                    # Output values in *metric* unit system by default.
                    # TODO: Make output unit system configurable.
                    "output_unit_system": "metric",
                }
            )
            processed_data = ProcessedData(config=config, data=data)
            data = {key: value.value for key, value in processed_data.output.items()}

        # This variant is compatible with earlier releases like `ecowitt2mqtt-2022.5.0`.
        except ImportError:
            import argparse

            from ecowitt2mqtt.data import DataProcessor

            args = argparse.Namespace()
            args.input_unit_system = "imperial"
            args.output_unit_system = "metric"
            args.raw_data = None

            data_processor = DataProcessor(data, args)
            data = data_processor.generate_data()

        return data
