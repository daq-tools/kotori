# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas.motl@elmyra.de>
# (c) 2017 Richard Pobering <einsiedlerkrebs@ginnungagap.org>
import time
import json
import requests
import Geohash
import paho.mqtt.client as mqtt
from geopy.geocoders import Nominatim
from pprint import pformat
"""
Request data from live API of luftdaten.info, enrich geospatial information and publish to MQTT bus.

See also: https://github.com/opendata-stuttgart/sensors-software/issues/33#issuecomment-272711445

Install prerequisites::

    pip install requests paho-mqtt Geohash geopy

Synopsis::

    python kotori/vendor/luftdaten/api_to_mqtt.py

Result::

    mosquitto_sub -h luftdaten.getkotori.org -t 'luftdaten/testdrive/#' -v
    luftdaten/testdrive/earth/42/data.json {"sensor_id": 778, "location_name": "Alte Landstra\u00dfe, Bludesch, Vorarlberg, AT", "temperature": 18.9, "time": "2017-03-29T15:29:02", "geohash": "u0qutbdmbb5s", "location_id": 372, "humidity": 43.2}
    luftdaten/testdrive/earth/42/data.json {"sensor_id": 1309, "location_name": "Unterer Rosberg, Waiblingen, Baden-W\u00fcrttemberg, DE", "temperature": 27.7, "time": "2017-03-29T15:29:02", "geohash": "u0wtgfygz1rr", "location_id": 647, "humidity": 1.0}
    [...]

"""

# Configuration
api_url     = 'https://api.luftdaten.info/static/v1/data.json'
mqtt_broker = 'luftdaten.getkotori.org'

backend = mqtt.Client(client_id='42', clean_session=True)
backend.connect(mqtt_broker)

def request_and_publish():
    payload = requests.get(api_url).content
    data = json.loads(payload)
    #pprint(data)

    for item in data:

        print '-' * 42

        timestamp = item['timestamp']
        location_id = item['location']['id']
        sensor_id = item['sensor']['id']
        readings = {}
        for sensor in item['sensordatavalues']:
            name = sensor['value_type']
            value = float(sensor['value'])
            readings[name] = value

        address = {
            'location_id': location_id,
            'sensor_id': sensor_id,
        }

        readings['time'] = timestamp
        readings['geohash'] = geohash(item['location']['latitude'], item['location']['longitude'])
        readings['location_name'] = reverse_geocode(item['location']['latitude'], item['location']['longitude'])
        readings.update(address)

        publish_mqtt(address, readings)

def geohash(latitude, longitude):
    return Geohash.encode(float(latitude), float(longitude))

# TODO: Use memoization! Maybe cache into MongoDB as well using Beaker.
# Or use a local version of Nomatim: https://wiki.openstreetmap.org/wiki/Nominatim/Installation
def reverse_geocode(latitude, longitude):
    try:
        geolocator = Nominatim()
        position_string = '{}, {}'.format(float(latitude), float(longitude))
        location = geolocator.reverse(position_string)
        # Fair use!
        time.sleep(1)
    except Exception as ex:
        print 'Error when reverse geocoding: {}. lat={}, lon={}'.format(ex, latitude, longitude)
        return ''

    print 'DEBUG:\n', pformat(location.raw)

    # Be agnostic against city vs. village
    # TODO: Handle Rgbg
    address = location.raw['address']
    if 'city' not in address:
        if 'village' in address:
            address['city'] = address['village']
        elif 'town' in address:
            address['city'] = address['town']
        elif 'county' in address:
            address['city'] = address['county']
        elif 'suburb' in address:
            address['city'] = address['suburb']
        elif 'city_district' in address:
            address['city'] = address['city_district']

    # Add more convenience for handling Stadtstaaten
    if 'city' in address and 'state' in address and address['city'] == address['state']:
        if 'suburb' in address:
            address['city'] = address['suburb']
        elif 'city_district' in address:
            address['city'] = address['city_district']

    # TODO: Maybe use neighbourhood vs. suburb vs. city_district
    # TODO: Handle "building"

    # Be agnostic against road vs. path
    if 'road' not in address:
        if 'path' in address:
            address['road'] = address['path']
        elif 'cycleway' in address:
            address['road'] = address['cycleway']

    # Uppercase country code
    address['country_code'] = address['country_code'].upper()

    address_fields = ['road', 'city', 'state', 'country_code']
    address_parts = []
    for address_field in address_fields:
        if address_field in address:
            address_parts.append(address[address_field])

    try:
        location_label = ', '.join(address_parts).encode('utf-8')
        return location_label
    except Exception as ex:
        print 'Error formatting location name: {}. location.raw: {}'.format(ex, location.raw)
        return ''

def publish_mqtt(address, measurement):

    # MQTT bus topic
    mqtt_topic_template = u'{realm}/{network}/{gateway}/{node}/{kind}.json'
    mqtt_address = dict(
        realm   = 'luftdaten',
        network = 'testdrive',
        gateway = 'earth',
        node    = '42',
    )
    #gateway = 'l' + str(address['location_id']),
    #node    = address['sensor_id']

    # define data and event type
    mqtt_data_topic  = mqtt_topic_template.format(kind='data', **mqtt_address)
    mqtt_message = json.dumps(measurement)

    print 'Publishing to {topic}: {message}'.format(topic=mqtt_data_topic, message=mqtt_message)

    backend.publish(mqtt_data_topic, mqtt_message)

def main():
    request_and_publish()

if __name__ == '__main__':
    main()
