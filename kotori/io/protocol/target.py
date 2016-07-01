# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl <andreas.motl@elmyra.de>
from twisted.internet import threads
from twisted.web import http, server
from twisted.logger import Logger
from twisted.application.service import MultiService
from kotori.configuration import read_list
from kotori.daq.services import MultiServiceMixin
from kotori.daq.intercom.mqtt import MqttAdapter
from kotori.io.protocol.http import HttpDataFrameResponse
from kotori.io.protocol.influx import DataFrameQuery
from kotori.io.protocol.util import handleFailure

log = Logger()

class ForwarderTargetService(MultiServiceMixin, MultiService):
    """
    Container service for target services.

    As of June 2016, there are currently two target
    services for emitting data, MQTT and InfluxDB.
    """

    def __init__(self, address=None, **kwargs):
        MultiServiceMixin.__init__(self, **kwargs)

        self.address = address
        self.scheme  = self.address.uri.scheme

        self.downstream = None

    def setupService(self):
        """
        Configure effective data target by registering an appropriate
        downstream service object for handling the target address scheme.
        """

        log.info(u'Starting {name} for serving address {address}', name=self.logname, address=self.address)

        self.settings = self.parent.settings

        if self.scheme == 'mqtt':

            # Register MqttAdapter service as downstream subsystem service object
            self.downstream = MqttAdapter(
                name          = self.name + '-downstream',
                broker_host   = self.settings.mqtt.host,
                broker_port   = int(self.settings.mqtt.port))

        elif self.scheme == 'influxdb':
            # InfluxDB has no subsystem service, it's just an adapter
            pass

        else:
            raise KeyError('No target/downstream dispatcher for scheme {scheme}'.format(scheme=self.scheme))

        # Register service component with its container
        if self.downstream:
            self.registerService(self.downstream)

    def emit(self, uri, bucket):
        """
        Adapt, serialize and emit data bucket to target service.
        """

        log.info('Emitting to target scheme {scheme}', scheme=self.scheme)

        if self.scheme == 'mqtt':

            # Publish JSON payload to MQTT bus
            topic   = uri
            payload = bucket.json
            return self.downstream.publish(topic, payload)

        elif self.scheme == 'influxdb':

            # InfluxDB query wrapper using expression derived from transformation data
            dfq = DataFrameQuery(settings=self.settings, bucket=bucket)

            # Perform query and obtain results as pandas DataFrame
            df = dfq.query()

            # Announce routing information via http response headers
            bucket.request.setHeader('Target-Database', bucket.tdata.database)
            bucket.request.setHeader('Target-Expression', bucket.tdata.expression)
            bucket.request.setHeader('Target-Address-Scheme', self.scheme)
            bucket.request.setHeader('Target-Address-Uri', uri)

            # Database result is empty, send appropriate response
            if df is None or df.empty:
                return self.response_no_results(bucket)

            # Drop some fields from DataFrame as requested
            if 'exclude' in bucket.tdata and bucket.tdata.exclude:
                drop_fields = read_list(bucket.tdata.exclude)
                try:
                    df.drop(drop_fields, axis=1, inplace=True)
                except ValueError as ex:
                    error_message = u'Error: {message}'.format(message=ex)
                    return bucket.request.error_response(bucket, error_message=error_message)

            # Compute http response from DataFrame, taking designated output format into account
            response = HttpDataFrameResponse(bucket, dataframe=df)

            # Synchronous
            #return response.render()

            # Asynchronous: Perform computation in separate thread
            d = threads.deferToThread(response.render)
            d.addErrback(handleFailure, bucket)
            d.addBoth(bucket.request.write)
            d.addBoth(lambda _: bucket.request.finish())
            return server.NOT_DONE_YET


        else:
            message = 'No target/downstream dispatcher for scheme {scheme}'.format(scheme=self.scheme)
            log.error(message)
            raise KeyError(message)

    def response_no_results(self, bucket):
        """
        Send "404 Not Found" response body in text/plain
        format describing HTTP API query interface.
        """
        # FIXME: Some words about "now-10d" being the default for "from", see influx.py.
        # FIXME: Maybe refactor "now-10d" to transformation machinery to make it accessible from here.
        error_message = u'# 404 Not Found\n#\n'\
                        u'# No data for query expression "{expression}"\n'\
                        u'# Please recognize absolute datetimes are expected to be in ISO 8601 format. '\
                        u'Default is UTC, optionally specify an appropriate timezone offset.\n'.format(expression=bucket.tdata.expression)
        error_message += u'#\n# Examples:\n#\n'\
                         u'#   ?from=2016-06-25T22:00:00.000Z\n'\
                         u'#   ?from=2016-06-26T00:00:00.000%2B02:00    (%2B is "+" urlencoded)\n'\
                         u'#   ?from=now-4h&to=now-2h\n'\
                         u'#   ?from=now-8d5h3m&to=now-6d'
        bucket.request.setResponseCode(http.NOT_FOUND)
        bucket.request.setHeader('Content-Type', 'text/plain; charset=utf-8')
        return error_message.encode('utf-8')

