# -*- coding: utf-8 -*-
# (c) 2017,2018 Andreas Motl <andreas@hiveeyes.org>
# (c) 2017,2018 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import time
import json
import logging

import appdirs
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
==============
Luftdatenpumpe
==============


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

    luftdatenpumpe forward --mqtt-uri mqtt://mqtt.example.org/luftdaten.info --progress

    2017-04-22 03:53:47,947 [kotori.vendor.luftdaten.luftdatenpumpe] INFO   : Publishing data to MQTT URI mqtt://mqtt.example.org/luftdaten.info
    2017-04-22 03:53:49,012 [kotori.vendor.luftdaten.luftdatenpumpe] INFO   : Timestamp of first record: 2017-04-22T01:48:02Z
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

    luftdatenpumpe forward --mqtt-uri mqtt://username:password@mqtt.example.org/luftdaten.info


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

    luftdatenpumpe forward --mqtt-uri mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json --geohash --reverse-geocode --progress

    2017-04-22 03:55:50,426 [kotori.vendor.luftdaten.luftdatenpumpe] INFO   : Publishing data to MQTT URI mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json
    2017-04-22 03:55:51,396 [kotori.vendor.luftdaten.luftdatenpumpe] INFO   : Timestamp of first record: 2017-04-22T01:50:02Z
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

# Configure cache for responses from Nominatim
cache_path = os.path.join(appdirs.user_cache_dir(appname='luftdaten.info', appauthor=False), 'nominatim')
cache_options = {
    'type': 'file',
    'data_dir': os.path.join(cache_path, 'data'),
    'lock_dir': os.path.join(cache_path, 'lock'),
}
cache = CacheManager(**cache_options)

APP_NAME    = 'luftdatenpumpe'
APP_VERSION = '0.2.1'

def main():
    """
    Usage:
      luftdatenpumpe forward --mqtt-uri mqtt://mqtt.example.org/luftdaten.info [--geohash] [--reverse-geocode] [--progress] [--sensors=<sensors>] [--locations=<locations>] [--debug] [--dry-run]
      luftdatenpumpe --version
      luftdatenpumpe (-h | --help)

    Options:
      --mqtt-uri=<mqtt-uri>         Use specified MQTT broker
      --geohash                     Compute Geohash from latitude/longitude and add to MQTT message
      --reverse-geocode             Compute geographical address using the Nominatim reverse geocoder and add to MQTT message
      --progress                    Show progress bar
      --sensors=<sensors>           Filter data by given sensor ids, comma-separated.
      --locations=<locations>       Filter data by given location ids, comma-separated.
      --version                     Show version information
      --dry-run                     Run data acquisition and postprocessing but skip publishing to MQTT bus
      --debug                       Enable debug messages
      -h --help                     Show this screen

    Examples:

      # Publish data to topic "luftdaten.info" at MQTT broker "mqtt.example.org"
      luftdatenpumpe forward --mqtt-uri mqtt://mqtt.example.org/luftdaten.info

      # Publish fully enriched data for multiple sensor ids
      luftdatenpumpe forward --mqtt-uri mqtt://mqtt.example.org/luftdaten.info --geohash --reverse-geocode --sensors=2115,2116

      # Publish fully enriched data for multiple location ids
      luftdatenpumpe forward --mqtt-uri mqtt://mqtt.example.org/luftdaten.info --geohash --reverse-geocode --locations=1064,1071

      # Publish data suitable for displaying in Grafana Worldmap Panel using Kotori
      luftdatenpumpe forward --mqtt-uri mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json --geohash --reverse-geocode --progress

    """

    # Parse command line arguments
    options = docopt(main.__doc__, version=APP_NAME + ' ' + APP_VERSION)
    #print 'options: {}'.format(options)

    debug = options.get('--debug')

    # Setup logging
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Run
    log.info('Nominatim cache path is {}'.format(cache_path))

    # Optionally, apply filters by sensor id and location id
    filter = {}
    for filter_name in ['locations', 'sensors']:
        filter_option = '--' + filter_name
        if options[filter_option]:
            filter[filter_name] = map(int, options[filter_option].replace(' ', '').split(','))

    elif options['forward']:

        mqtt_uri = options.get('--mqtt-uri')
        if not mqtt_uri:
            log.critical('Parameter "--mqtt-uri" missing or empty')
            sys.exit(1)

        log.info('Will publish to MQTT at {}'.format(mqtt_uri))

        pump = LuftdatenPumpe(
            mqtt_uri,
            geohash=options['--geohash'],
            reverse_geocode=options['--reverse-geocode'],
            dry_run=options['--dry-run'],
            progressbar=options['--progress'],
            filter=filter
        )
        pump.request_and_publish()


class LuftdatenPumpe:

    # luftdaten.info API URI
    uri = 'https://api.luftdaten.info/static/v1/data.json'

    def __init__(self, mqtt_uri, geohash=False, reverse_geocode=False, dry_run=False, progressbar=False, filter=None):
        self.mqtt_uri = mqtt_uri
        self.geohash = geohash
        self.reverse_geocode = reverse_geocode
        self.dry_run = dry_run
        self.progressbar = progressbar
        self.filter = filter
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

            # If there is a filter defined, evaluate it
            # For specific location|sensor ids, skip further processing
            if self.filter:
                if 'locations' in self.filter:
                    if location_id not in self.filter['locations']:
                        continue
                if 'sensors' in self.filter:
                    if sensor_id not in self.filter['sensors']:
                        continue

            # Collect readings
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
                try:
                    readings['location_name'] = reverse_geocode(item['location']['latitude'], item['location']['longitude'])
                except Exception as ex:
                    pass

            # Publish to MQTT bus
            if self.dry_run:
                log.info('Dry-run. Would publish record:\n{}'.format(pformat(readings)))
            else:
                self.publish_mqtt(readings)

            # Debugging
            #break

    @staticmethod
    def convert_timestamp(timestamp):
        # mungle timestamp to be formally in ISO 8601/UTC
        if ' ' in timestamp:
            timestamp = timestamp.replace(' ', 'T')
        if '+' not in timestamp:
            timestamp += 'Z'
        return timestamp

    def publish_mqtt(self, measurement):
        # FIXME: Don't only use ``sort_keys``. Also honor the field names of the actual readings by
        # putting them first. This is:
        # - "P1" and "P2" for "sensor_type": "SDS011"
        # - "temperature" and "humidity" for "sensor_type": "DHT22"
        # - "temperature", "humidity", "pressure" and "pressure_at_sealevel" for "sensor_type": "BME280"
        mqtt_message = json.dumps(measurement, sort_keys=True)
        self.mqtt.publish(mqtt_message)


def geohash(latitude, longitude):
    return Geohash.encode(float(latitude), float(longitude))


# Cache responses from Nominatim for 3 months
@cache.cache(expire = 60 * 60 * 24 * 30 * 3)
def reverse_geocode(latitude, longitude):
    """
    # Done: Use memoization! Maybe cache into MongoDB as well using Beaker.
    # TODO: Or use a local version of Nomatim: https://wiki.openstreetmap.org/wiki/Nominatim/Installation
    """
    try:
        # 2018-03-24
        # Nominatim expects the User-Agent as HTTP header otherwise it returns a HTTP-403.
        # This has been fixed in geopy-1.12.0.
        # https://operations.osmfoundation.org/policies/nominatim/
        # https://github.com/geopy/geopy/issues/185
        geolocator = Nominatim(user_agent=APP_NAME + '/' + APP_VERSION)

        # FIXME: When using "HTTP_PROXY" from environment, use scheme='http'
        # export HTTP_PROXY=http://weather.hiveeyes.org:8912/
        # See also https://github.com/geopy/geopy/issues/263
        #geolocator = Nominatim(user_agent=APP_NAME + '/' + APP_VERSION, scheme='http')

        position_string = '{}, {}'.format(float(latitude), float(longitude))
        location = geolocator.reverse(position_string)
    except Exception as ex:
        name = ex.__class__.__name__
        log.error('Reverse geocoding failed: {}: {}. lat={}, lon={}'.format(name, ex, latitude, longitude))
        raise
    finally:
        # Obey to fair use policy (an absolute maximum of 1 request per second).
        # https://operations.osmfoundation.org/policies/nominatim/
        time.sleep(1)

    #log.debug(u'Reverse geocoder result: {}'.format(pformat(location.raw)))

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
        - neighbourhood vs. quarter vs. residential vs. suburb vs. city_district vs. city vs. allotments

    How to handle "building", "public_building", "residential", "pedestrian", "kindergarten", "clothes"?
    """

    # Be agnostic against road vs. path
    if 'road' not in address:
        road_choices = ['path', 'pedestrian', 'cycleway', 'footway']
        for field in road_choices:
            if field in address:
                address['road'] = address[field]

    # Uppercase country code
    address['country_code'] = address['country_code'].upper()

    # Build display location from components
    address_fields = ['road', 'suburb', 'city', 'state', 'country_code']
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
