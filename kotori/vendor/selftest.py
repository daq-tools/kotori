# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@getkotori.org>
import json
import delegator

def publish(topic, message):
    command = 'mosquitto_pub -h "{host}" -t "{topic}" -m \'{message}\''.format(
        host='localhost', topic=topic, message=message)

    print 'Running command: {}'.format(command)
    delegator.run(command)

def all_realms():
    #realms = ['mqttkit-1', 'hiveeyes', 'luftdaten', 'weewx']
    realms = ['hiveeyes']
    measurements = {"temperature": 42.84, "weight": 84.85}
    for realm in realms:
        topic = '{}/testdrive/area-42/node-1/data.json'.format(realm)
        publish(topic, json.dumps(measurements))

def run():

    # Publish something to all configured realms
    #all_realms()

    # Publish something to the "hiveeyes" realm
    data = json.dumps({u'Gewicht 1': 5.0, u'Gewicht Total': 42.42, u'Außentemperatur': 32.32})
    publish('hiveeyes/testdrive/area-42/node-1/data.json', data)
