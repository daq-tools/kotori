# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@getkotori.org>
import os
import json


def publish(topic, message):
    command = 'mosquitto_pub -h "{host}" -t "{topic}" -m \'{message}\''.format(
        host='localhost', topic=topic, message=message)

    print('Running command: {}'.format(command))
    os.system(command)


def all_realms():
    #realms = ['mqttkit-1', 'hiveeyes', 'luftdaten', 'weewx']
    realms = ['hiveeyes']
    measurements = {"temperature": 42.84, "weight": 84.85}
    for realm in realms:
        topic = '{}/testdrive/area-42/node-1/data.json'.format(realm)
        publish(topic, json.dumps(measurements))


def hiveeyes_testcases():

    # Publish en bloc using German field names
    #data = json.dumps({u'Gewicht 1': 5.0, u'Gewicht Total': 42.42, u'Außentemperatur': 32.32})
    #publish('hiveeyes/testdrive/area-42/node-1/data.json', data)

    # Don't confuse field name classifier
    #data = json.dumps({u'Weight Total StdDev': 42.42, u'Weight Total': 42.42, u'Temperature 8 Outside': 32.32})
    #publish('hiveeyes/testdrive/area-42/node-2/data.json', data)

    # Publish discrete values I (from deprecated firmware)
    """
    hiveeyes/kh/cfb/hive1/measure/weight   55.435
    hiveeyes/kh/cfb/hive1/measure/broodtemperature  35.2
    hiveeyes/kh/cfb/hive1/measure/entrytemperature   6.6
    hiveeyes/kh/cfb/hive1/measure/airtemperature  21.7
    hiveeyes/kh/cfb/hive1/measure/airhumidity  58.5
    hiveeyes/kh/cfb/hive1/measure/airtemperature_outside (null)
    hiveeyes/kh/cfb/hive1/measure/airhumidity_outside (null)
    """
    #publish('hiveeyes/testdrive/area-42/node-3/measure/weight', 55.435)
    #publish('hiveeyes/testdrive/area-42/node-3/measure/airtemperature', 21.7)

    # Publish discrete values II (via LoRaWAN/TTN)
    """
    hiveeyes/thias/thias-hive2/up/data/relative_humidity_2 51.5
    hiveeyes/thias/thias-hive2/up/data/analog_in_3 3.5
    hiveeyes/thias/thias-hive2/up/data/analog_in_1 -13.54
    hiveeyes/thias/thias-hive2/up/data/temperature_1 21.1
    hiveeyes/thias/thias-hive2/up/data/relative_humidity_1 48.5
    hiveeyes/thias/thias-hive2/up/data/temperature_2 20.8
    """
    #publish('hiveeyes/testdrive/area-42/node-4/data/analog_in_3', 3.5)
    #publish('hiveeyes/testdrive/area-42/node-4/data/temperature_1', 21.1)


    # Special characters in topic name
    """
    data = json.dumps({"Weight Total StdDev": -0.017, "Temperature 3 Inside": "  7.00", "Humidity Outside": "99.90",
                       "Temperature 8 Outside": "3.60", "Temperature 1 Inside": "  6.69", "Temperature 2 Inside": "  3.56",
                       "Yield Sum": -0.821, "Weight Total": 25.599, "Weight 1": 4.827, "Weight 2": 8.45, "Weight 3": 5.202,
                       "Weight 4": 7.12})
    publish('hiveeyes/testdrive/area@42/node-5/data.json', data)
    """


def run():

    # Publish something to all configured realms
    #all_realms()

    # Runbook for some acquisition feeds arriving for the "hiveeyes" realm
    #hiveeyes_testcases()

    # weewx problem
    # 2018-04-09T07:20:15+0200 [kotori.daq.services.mig            ] WARN    : Unknown message type on topic "pressure_mbar" with payload "937.860347662"
    # weewx/097287c4-6fb0-4aeb-a095-00d65ecb15f7/Leoni/VantagePro2/pressure_mbar 937.860347662
    publish('weewx/testdrive/area-42/node-1/pressure_mbar', 937.860347662)
