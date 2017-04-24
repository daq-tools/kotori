# -*- coding: utf-8 -*-
# Copyright (c) 2017 Andreas Motl <andreas@getkotori.org>
# Copyright (c) 2017 Richard Pobering <richard@hiveeyes.org>
import os
import sys
import time
import json
import logging
import requests
import Geohash
import paho.mqtt.client as mqtt
from tqdm import tqdm
from docopt import docopt
from pprint import pformat
from urlparse import urlsplit
from beaker.cache import CacheManager
from geopy.geocoders import Nominatim
"""
=================
luftdaten-to-mqtt
=================


About
=====
Request data from live API of luftdaten.info, enrich with geospatial information and publish to MQTT bus.


References
==========
- http://luftdaten.info/
- http://archive.luftdaten.info/
- http://deutschland.maps.luftdaten.info/
- https://getkotori.org/docs/applications/luftdaten.info/
- https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-worldmap-prototype

.. seealso::

    `Support for InfluxDB and MQTT as backend <https://github.com/opendata-stuttgart/sensors-software/issues/33#issuecomment-272711445>`_.


Setup
=====
Install Python modules::

    pip install docopt==0.6.2 requests==2.13.0 paho-mqtt==1.2 Geohash==1.0 geopy==1.11.0 Beaker==1.8.1 tqdm==4.11.2


Synopsis
========
::

    luftdaten-to-mqtt --mqtt-uri mqtt://mqtt.example.org/luftdaten.info --progress

    2017-04-22 03:53:47,947 [kotori.vendor.luftdaten.luftdaten_api_to_mqtt] INFO   : Publishing data to MQTT URI mqtt://mqtt.example.org/luftdaten.info
    2017-04-22 03:53:49,012 [kotori.vendor.luftdaten.luftdaten_api_to_mqtt] INFO   : Timestamp of first record: 2017-04-22T01:48:02Z
    100%|..........................................................................| 6617/6617 [00:01<00:00, 4184.30it/s]

Result (reformatted for better readability)::

    mosquitto_sub -h mqtt.example.org -t 'luftdaten.info/#' -v

    /luftdaten.info {"humidity": 42.2, "temperature": 12.0,     "location_id":  49, "sensor_id":  418, "sensor_type": "DHT22",  "time": "2017-04-21 23:49:01"}
    /luftdaten.info {"P1": 7.5, "P2": 6.42,                     "location_id": 919, "sensor_id": 1799, "sensor_type": "SDS011", "time": "2017-04-21 23:49:01"}
    # [...]


Advanced usage
==============


With authentication
-------------------
::

    luftdaten-to-mqtt --mqtt-uri mqtt://username:password@mqtt.example.org/luftdaten.info


WAN topology
------------
WAN addressing with geospatial data enrichment::

    --geohash                 Compute Geohash from latitude/longitude and add to MQTT message
    --reverse-geocode         Compute geographical address using the Nominatim reverse geocoder and add to MQTT message

Suitable for data acquisition with Kotori and InfluxDB. Display with Grafana Worldmap Panel.

.. seealso::

    - https://github.com/vinsci/geohash/
    - https://github.com/openstreetmap/Nominatim
    - https://github.com/daq-tools/kotori
    - https://github.com/influxdata/influxdb
    - https://github.com/grafana/grafana
    - https://grafana.com/plugins/grafana-worldmap-panel

Publisher::

    luftdaten-to-mqtt --mqtt-uri mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json --geohash --reverse-geocode --progress

    2017-04-22 03:55:50,426 [kotori.vendor.luftdaten.luftdaten_api_to_mqtt] INFO   : Publishing data to MQTT URI mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json
    2017-04-22 03:55:51,396 [kotori.vendor.luftdaten.luftdaten_api_to_mqtt] INFO   : Timestamp of first record: 2017-04-22T01:50:02Z
    100%|..........................................................................| 6782/6782 [01:01<00:00, 109.77it/s]

Subscriber::

    mosquitto_sub -h mqtt.example.org -t 'luftdaten/testdrive/#' -v

    luftdaten/testdrive/earth/42/data.json {"sensor_id": 778,  "location_name": "Alte Landstra\u00dfe, Bludesch, Vorarlberg, AT",          "temperature": 18.9, "time": "2017-03-29T15:29:02", "geohash": "u0qutbdmbb5s", "location_id": 372, "humidity": 43.2}
    luftdaten/testdrive/earth/42/data.json {"sensor_id": 1309, "location_name": "Unterer Rosberg, Waiblingen, Baden-W\u00fcrttemberg, DE", "temperature": 27.7, "time": "2017-03-29T15:29:02", "geohash": "u0wtgfygz1rr", "location_id": 647, "humidity": 1.0}
    # [...]


License
=======

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, see:
   <http://www.gnu.org/licenses/gpl-3.0.txt>,
   or write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

"""



log = logging.getLogger(__name__)

cache_options = {
    'type': 'file',
    'data_dir': '/var/cache/nominatim/data',
    'lock_dir': '/var/cache/nominatim/lock'
}
if sys.platform == 'darwin':
    cache_options = {
        'type': 'file',
        'data_dir': '/tmp/nominatim-cache/data',
        'lock_dir': '/tmp/nominatim-cache/lock'
    }
cache = CacheManager(**cache_options)

VERSION  = '0.1.0'
APP_NAME = 'luftdaten-to-mqtt ' + VERSION

def main():
    """
    Usage:
      luftdaten-to-mqtt --mqtt-uri mqtt://mqtt.example.org/luftdaten.info [--geohash] [--reverse-geocode] [--progress] [--debug]
      luftdaten-to-mqtt --version
      luftdaten-to-mqtt (-h | --help)

    Options:
      --mqtt-uri=<mqtt-uri>     Use specified MQTT broker
      --geohash                 Compute Geohash from latitude/longitude and add to MQTT message
      --reverse-geocode         Compute geographical address using the Nominatim reverse geocoder and add to MQTT message
      --progress                Show progress bar
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    Examples:

      # Publish data to topic "luftdaten.info" at MQTT broker "mqtt.example.org"
      luftdaten-to-mqtt --mqtt-uri mqtt://mqtt.example.org/luftdaten.info

      # Publish data suitable for displaying in Grafana Worldmap Panel using Kotori
      luftdaten-to-mqtt --mqtt-uri mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json --geohash --reverse-geocode --progress

    """

    # Parse command line arguments
    options = docopt(main.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    debug = options.get('--debug')

    # Setup logging
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    mqtt_uri = options.get('--mqtt-uri')
    if not mqtt_uri:
        log.critical('Parameter "--mqtt-uri" missing or empty')
        sys.exit(1)

    # Run
    log.info('Publishing data to MQTT URI {}'.format(mqtt_uri))
    pump = LuftdatenPumpe(
        mqtt_uri,
        geohash=options['--geohash'],
        reverse_geocode=options['--reverse-geocode'],
        progressbar=options['--progress']
    )
    pump.request_and_publish()


class LuftdatenPumpe:

    # luftdaten.info API URI
    uri = 'https://api.luftdaten.info/static/v1/data.json'

    def __init__(self, mqtt_uri, geohash=False, reverse_geocode=False, progressbar=False):
        self.mqtt_uri = mqtt_uri
        self.geohash = geohash
        self.reverse_geocode = reverse_geocode
        self.progressbar = progressbar
        self.mqtt = MQTTAdapter(mqtt_uri)

    def request_and_publish(self):
        payload = requests.get(self.uri).content
        data = json.loads(payload)
        #pprint(data)

        timestamp = self.convert_timestamp(data[0]['timestamp'])
        log.info('Timestamp of first record: {}'.format(timestamp))

        iterator = data
        if self.progressbar:
            iterator = tqdm(data)

        for item in iterator:

            # Decode JSON item
            timestamp = item['timestamp']
            location_id = item['location']['id']
            sensor_id = item['sensor']['id']
            sensor_type = item['sensor']['sensor_type']['name']
            readings = {}
            for sensor in item['sensordatavalues']:
                name = sensor['value_type']
                value = float(sensor['value'])
                readings[name] = value

            readings['time'] = self.convert_timestamp(timestamp)

            sensor_address = {
                'location_id': location_id,
                'sensor_id':   sensor_id,
                'sensor_type': sensor_type,
            }
            readings.update(sensor_address)

            if self.geohash:
                readings['geohash'] = geohash(item['location']['latitude'], item['location']['longitude'])

            if self.reverse_geocode:
                readings['location_name'] = reverse_geocode(item['location']['latitude'], item['location']['longitude'])

            self.publish_mqtt(readings)

    @staticmethod
    def convert_timestamp(timestamp):
        # mungle timestamp to be formally in ISO 8601/UTC
        if ' ' in timestamp:
            timestamp = timestamp.replace(' ', 'T')
        if '+' not in timestamp:
            timestamp += 'Z'
        return timestamp

    def publish_mqtt(self, measurement):
        mqtt_message = json.dumps(measurement, sort_keys=True)
        self.mqtt.publish(mqtt_message)

def geohash(latitude, longitude):
    return Geohash.encode(float(latitude), float(longitude))


# Cache responses from Nominatim for 1 month
@cache.cache(expire = 60 * 60 * 24 * 30)
def reverse_geocode(latitude, longitude):
    """
    # Done: Use memoization! Maybe cache into MongoDB as well using Beaker.
    # TODO: Or use a local version of Nomatim: https://wiki.openstreetmap.org/wiki/Nominatim/Installation
    """
    try:
        geolocator = Nominatim()
        position_string = '{}, {}'.format(float(latitude), float(longitude))
        location = geolocator.reverse(position_string)
        # Fair use!
        time.sleep(1)
    except Exception as ex:
        log.error('Reverse geocoding failed: {}. lat={}, lon={}'.format(ex, latitude, longitude))
        return ''

    #log.debug('Reverse geocoder: {}'.format(pformat(location.raw)))

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

        # Stadtstaat FTW!
        elif 'state' in address:
            address['city'] = address['state']

    # Add more convenience for handling Stadtstaaten
    if 'city' in address and 'state' in address and address['city'] == address['state']:
        if 'suburb' in address:
            address['city'] = address['suburb']
        elif 'city_district' in address:
            address['city'] = address['city_district']

    # Stadtteil FTW
    if 'suburb' not in address and 'residential' in address:
        address['suburb'] = address['residential']

    """
    Get this sorted: https://wiki.openstreetmap.org/wiki/Key:place !!!
    Get urban vs. rural sorted out

    1. country
    2. state
    3. "Überregional": "q-region"
        - county, state_district, state
    4. "Regional": "q-hood"
        - neighbourhood vs. quarter vs. residential vs. suburb vs. city_district vs. city

    How to handle "building", "public_building", "residential", "pedestrian", "kindergarten", "clothes"?
    """

    # Be agnostic against road vs. path
    if 'road' not in address:
        if 'path' in address:
            address['road'] = address['path']
        elif 'pedestrian' in address:
            address['road'] = address['pedestrian']
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


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-25s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)

    # TODO: Control debug logging of HTTP requests through yet another commandline option "--debug-http" or "--debug-requests"
    requests_log = logging.getLogger('requests')
    requests_log.setLevel(logging.WARN)


class MQTTAdapter(object):

    def __init__(self, uri, keepalive=60, client_id_prefix=None):

        address = urlsplit(uri)
        self.host       = address.hostname
        self.port       = address.port or 1883
        self.username   = address.username
        self.password   = address.password
        self.topic      = address.path

        self.keepalive  = keepalive

        self.client_id_prefix = client_id_prefix

        self.connect()

    def connect(self):

        # Create a mqtt client object
        pid = os.getpid()
        client_id = '{}:{}'.format(self.client_id_prefix, str(pid))
        self.mqttc = mqtt.Client(client_id=client_id, clean_session=True)

        # Handle authentication
        if self.username:
            self.mqttc.username_pw_set(self.username, self.password)

        # Connect to broker
        self.mqttc.connect(self.host, self.port, self.keepalive)

    def close(self):
        self.mqttc.disconnect()

    def effective_topic(self, topic=None):
        parts = []
        base_topic = self.topic.strip(u'/')
        if base_topic:
            parts.append(base_topic)
        if topic:
            parts.append(topic)
        return u'/'.join(parts)

    def publish(self, message, topic=None):
        topic = self.effective_topic(topic)
        log.debug('Publishing to topic "{}": {}'.format(topic, message))
        return self.mqttc.publish(topic, message)

    def subscribe(self, topic=None):
        topic = self.effective_topic(topic)
        log.info('Subscribing to topic "{}"'.format(topic))
        return self.mqttc.subscribe(topic)


if __name__ == '__main__':
    main()



"""
Example for DHT22 sensor::

    {
        "id": 59625316,
        "location": {
            "id": 312,
            "latitude": "48.647",
            "longitude": "9.445"
        },
        "sampling_rate": null,
        "sensor": {
            "id": 660,
            "pin": "7",
            "sensor_type": {
                "id": 9,
                "manufacturer": "various",
                "name": "DHT22"
            }
        },
        "sensordatavalues": [
            {
                "id": 169745466,
                "value": "44.30",
                "value_type": "humidity"
            },
            {
                "id": 169745465,
                "value": "15.80",
                "value_type": "temperature"
            }
        ],
        "timestamp": "2017-03-30T19:24:02"
    }

Example for SDS011 sensor::

    {
        "id": 59625314,
        "location": {
            "id": 220,
            "latitude": "48.741",
            "longitude": "9.317"
        },
        "sampling_rate": null,
        "sensor": {
            "id": 467,
            "pin": "1",
            "sensor_type": {
                "id": 14,
                "manufacturer": "Nova Fitness",
                "name": "SDS011"
            }
        },
        "sensordatavalues": [
            {
                "id": 169745461,
                "value": "6.73",
                "value_type": "P1"
            },
            {
                "id": 169745462,
                "value": "4.48",
                "value_type": "P2"
            }
        ],
        "timestamp": "2017-03-30T19:24:02"
    },

"""
