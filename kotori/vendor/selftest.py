# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@getkotori.org>
import json
import delegator

def run():
    realms = ['mqttkit-1', 'hiveeyes', 'luftdaten', 'weewx']
    measurements = {"temperature": 42.84, "weight": 84.85}
    for realm in realms:
        topic = '{}/testdrive/area-42/node-1/data.json'.format(realm)
        command = 'mosquitto_pub -h "{host}" -t "{topic}" -m \'{message}\''.format(
            host='localhost', topic=topic, message=json.dumps(measurements))

        print 'Running command: {}'.format(command)
        delegator.run(command)
