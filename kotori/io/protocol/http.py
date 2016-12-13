# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl <andreas.motl@elmyra.de>
import json
import types
import mimetypes
import txmongo
from six import BytesIO
from copy import deepcopy
from urlparse import urlparse
from bunch import bunchify, Bunch
from collections import OrderedDict
from twisted.application.service import Service
from twisted.internet import reactor, defer
from twisted.logger import Logger
from twisted.web import http, server
from twisted.web.http import parse_qs
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.error import Error
from twisted.python.compat import nativeString
from kotori.io.router.path import PathRoutingEngine
from kotori.io.export.tabular import UniversalTabularExporter
from kotori.io.export.plot import UniversalPlotter
from kotori.io.protocol.util import convert_floats, slugify_datettime, flatten_request_args, handleFailure
from kotori.errors import last_error_and_traceback

log = Logger()

class LocalSite(Site):

    def log(self, request):
        """
        Redirect logging of HTTPFactory.

        @param request: The request object about which to log.
        @type request: L{Request}
        """
        line = u'HTTP access: ' + self._logFormatter(self._logDateTime, request)
        if self._nativeize:
            line = nativeString(line)
        else:
            line = line.encode("utf-8")
        log.debug(line)

class HttpServerService(Service):
    """
    Singleton instance of a Twisted service wrapping
    the Twisted TCP/HTTP server object "Site", in turn
    obtaining a ``HttpChannelContainer`` as root resource.
    """

    _instance = None

    def __init__(self, settings):

        # Propagate global settings
        self.settings = settings

        # Unique name of this service
        self.name = 'http-server-default'

        # Root resource object representing a channel
        # Contains routing machinery
        self.root = HttpChannelContainer()

        # Forward route registration method to channel object
        self.registerEndpoint = self.root.registerEndpoint

    def startService(self):
        """
        Start TCP listener on designated HTTP port,
        serving ``HttpChannelContainer`` as root resource.
        """

        # Don't start service twice
        if self.running == 1:
            return

        self.running = 1

        # Prepare startup
        http_listen = self.settings.kotori.http_listen
        http_port   = int(self.settings.kotori.http_port)
        log.info('Starting HTTP service on {http_listen}:{http_port}', http_listen=http_listen, http_port=http_port)

        # Configure root Site object and start listening to requests.
        # This must take place only once - can't bind to the same port multiple times!
        factory = LocalSite(self.root)
        reactor.listenTCP(http_port, factory, interface=http_listen)

    @classmethod
    def create(cls, settings):
        """
        Singleton factory
        """
        if not cls._instance:
            cls._instance = HttpServerService(settings)
            cls._instance.startService()
        return cls._instance


class HttpChannelContainer(Resource):
    """
    Twisted Site HTTP root resource driven by a
    routing engine based on the Pyramid request router.
    """

    def __init__(self):
        Resource.__init__(self)

        log.info('HttpChannelContainer init')

        self.database_connect()

        self.router    = PathRoutingEngine()
        self.callbacks = {}

    @defer.inlineCallbacks
    def database_connect(self):
        """
        Connect to Metadata storage
        """
        log.info('Connecting to Metadata storage database (MongoDB)')
        mongodb_uri = "mongodb://localhost:27017"

        # TODO: Make MongoDB address configurable
        #self.metastore = yield txmongo.MongoConnection(mongodb_uri)
        self.metastore = yield txmongo.MongoConnection(host='localhost', port=27017)

    def registerEndpoint(self, methods=None, path=None, callback=None):
        """
        Register path/callback with routing engine.
        """
        methods = methods or []
        log.info('Registering endpoint at path {path} for methods {methods}', path=path, methods=methods)
        if not callable(callback):
            log.error('Reference to endpoint {path} specified via "callback" '
                      'argument is not callable: {callback}', path=path, callback=callback)
            return

        # TODO: Add sanity checks for protecting against collisions on "name" and "path"
        name = path
        self.router.add_route(name, path, methods=methods)
        self.callbacks[name] = callback

    def getChild(self, name, request):
        """
        Twisted Resource path traversal method using
        the Pyramid request router for matching
        the request to registered endpoints.

        Returns ``HttpChannelEndpoint`` instance on match.
        """

        #log.info('getChild: {name}', name=name)
        uri = urlparse(str(request.URLPath()))

        # router v1
        """
        for endpoint in self.endpoints:
            if uri.path.startswith(endpoint.path):
                return HttpChannelEndpoint(options=endpoint)
        """

        # router v2
        result = self.router.match(request.method, uri.path)
        if result:
            #print 'route match result:'; pprint(result)

            # Obtain matched route name
            route_name = result['route'].name

            # Obtain appropriate callback function
            # TODO: Beware of collisions on "route_name", see above
            callback = self.callbacks[route_name]

            # Wrap endpoint description into container object
            endpoint = bunchify({'path': route_name, 'callback': callback, 'match': result['match'], 'request': request})

            # Create leaf resource instance
            return HttpChannelEndpoint(options=endpoint, metastore=self.metastore)

        # If nothing matched, continue traversal
        return self


class HttpChannelEndpoint(Resource):
    """
    Upper layer of data forwarding workhorse for HTTP.

    Twisted Site HTTP leaf resource containing the main dispatcher
    logic for forwarding inbound requests to the routing target.
    """

    isLeaf = True

    def __init__(self, options, metastore=None):
        self.options = options
        self.metastore = metastore
        Resource.__init__(self)

    def render(self, request):
        """
        Main Twisted Resource rendering method,
        overridden to provide custom logic.
        """

        # Pluck ``error_response`` method to request object
        request.error_response = self.error_response

        # Pluck ``channel_identifier`` attribute to request object
        request.channel_identifier = request.path.replace('/api', '').replace('/data', '')

        # Pluck response messages object to request object
        request.messages = []

        # Add informational headers
        request.setHeader('Channel-Id', request.channel_identifier)

        # Main bucket data container object serving the whole downstream processing chain
        bucket = Bunch(path=request.path, request=request)

        # Dispatch request
        deferred = defer.Deferred()
        self.dispatch(bucket, deferred)

        # Establish callback processing chain
        deferred.addCallback(self.propagate_data, bucket)
        deferred.addErrback(handleFailure, request)
        deferred.addBoth(self.render_messages, request)
        deferred.addBoth(request.write)
        deferred.addBoth(lambda _: request.finish())

        return server.NOT_DONE_YET

    def render_messages(self, passthrough, request):
        if request.messages:
            request.setHeader('Content-Type', 'application/json')
            return json.dumps(request.messages, indent=4)
        else:
            request.setHeader('Content-Type', 'text/plain; charset=utf-8')
            return passthrough

    def dispatch(self, bucket, deferred):
        """
        Forward inbound requests to the routing target by performing these steps:

        - Build the transformation data container ``tdata``
          by feeding it information from the HTTP request:

            - Obtain HTTP request
            - Decode data from request body
            - Merge data from request arguments
            - Merge data from url matches

        - Build the main data container object ``bucket``
          serving the whole downstream processing chain.

        - Call designated registered callback method with ``bucket``.

        """

        request = bucket.request

        content_type = request.getHeader('Content-Type')
        log.debug('Received HTTP request on uri {uri}, '
                  'content type is "{content_type}"', uri=request.path, content_type=content_type)

        # Read and decode request body
        body = request.content.read()
        bucket.body = body

        # Decode data from request body
        if body:
            if content_type.startswith('application/json'):
                deferred.callback(json.loads(body))

            elif content_type.startswith('application/x-www-form-urlencoded'):
                # TODO: Honor charset when receiving "application/x-www-form-urlencoded; charset=utf-8"
                payload = parse_qs(body, 1)
                # TODO: Decapsulate multiple values of same reading into "{name}-{N}", where N=1...
                for key, value in payload.iteritems():
                    if type(value) is types.ListType:
                        payload[key] = value[0]
                deferred.callback(payload)

            elif content_type.startswith('text/csv'):

                if not self.metastore:
                    log.error('Generic decoding of CSV format requires metastore')

                # Prepare alias for metastore table
                csv_header_store = self.metastore.kotori['channel-csv-headers']

                # 1. Decode CSV header like '## weight,temperature, humidity' and remember for upcoming data readings
                def get_header_fields(channel_data, data_lines):

                    first_line = data_lines[0]
                    header_line = None
                    if first_line.startswith('## '):
                        header_line = first_line[3:].strip()
                        data_lines = data_lines[1:]
                    elif first_line.startswith('Date/Time') or first_line.startswith('Datum/Zeit'):
                        header_line = first_line
                        data_lines = data_lines[1:]

                    header_fields = None
                    if header_line:
                        header_line = header_line.replace('Date/Time', 'time').replace('Datum/Zeit', 'time')
                        header_fields = map(str.strip, header_line.split(','))
                        msg = u'CSV Header: fields={fields}, key={key}'.format(fields=header_fields, key=request.channel_identifier)
                        log.info(msg)
                        deferred = csv_header_store.update(
                                {"channel": request.channel_identifier},
                                {"$set": {"header_fields": header_fields}}, upsert=True, safe=True)

                        message = u'Received header fields {}'.format(header_fields)
                        request.messages.append({'type': 'info', 'message': message})

                    elif channel_data:
                        header_fields = channel_data['header_fields']

                    #print 'header_fields, data_lines:', header_fields, data_lines
                    return header_fields, data_lines

                class MissingFieldnames(Exception): pass

                # 2. Assume data, map to full-qualified payload
                def parse_data(channel_data):
                    data_raw = body.strip()
                    data_lines = map(str.strip, data_raw.split('\n'))
                    header_fields, data_lines = get_header_fields(channel_data, data_lines)
                    if not header_fields:
                        raise MissingFieldnames('Could not process data, please supply field names before sending readings')
                    data_list = []
                    for data_line in data_lines:
                        data_fields = map(str.strip, data_line.split(','))
                        #print 'header_fields, data_fields:', header_fields, data_fields
                        data = OrderedDict(zip(header_fields, data_fields))
                        data_list.append(data)
                    deferred.callback(data_list)

                def data_error(ex):
                    # Re-raise regular/non-custom exceptions 1:1
                    if ex.type not in (MissingFieldnames,):
                        deferred.errback(ex)
                        return
                    # Signal other exceptions as bad request
                    deferred.errback(Error(http.BAD_REQUEST, response=ex))

                d2 = csv_header_store.find_one(filter={"channel": request.channel_identifier})
                d2.addCallback(parse_data)
                d2.addErrback(data_error)

            else:
                msg = u"Unable to handle Content-Type '{content_type}'".format(content_type=content_type)
                log.warn(msg)
                deferred.errback(Error(http.UNSUPPORTED_MEDIA_TYPE, response=msg))

        else:
            msg = u'Empty request body'
            log.warn(msg)
            deferred.errback(Error(http.BAD_REQUEST, response=msg))

    def propagate_data(self, data, bucket):

        # Main transformation data container
        bucket.tdata = Bunch()

        # Merge request parameters (GET and POST) and url matches, in this order
        bucket.tdata.update(flatten_request_args(bucket.request.args))
        bucket.tdata.update(self.options.match)

        #print 'propagate_data:', data
        if type(data) is not types.ListType:
            data = [data]

        response = None
        for item in data:
            # TODO: Apply this to telemetry values only!
            # FIXME: This is a hack
            if 'firmware' not in self.options.path:
                convert_floats(item, integers=['time'])
            response = self.propagate_single(item, bucket)

        message = 'Received #{number} readings'.format(number=len(data))
        bucket.request.messages.append({'type': 'info', 'message': message})

        # FIXME: This is nasty, but it's how Twisted works
        # NOT_DONE_YET = 1 (types.IntType)
        if isinstance(response, (bytes, types.IntType)):
            return response

    def propagate_single(self, item, bucket):

        # Serialize as json for convenience
        # TODO: Really?
        item_json = json.dumps(item)

        # Update main bucket container
        bucket.data = item
        bucket.json = item_json

        # Run forwarding callback
        return self.options.callback(bucket)

    @staticmethod
    def error_response(bucket, error_message='', code=http.BAD_REQUEST, with_traceback=False):
        """
        Error handling method logging and returning appropriate stacktrace.
        """
        # FIXME: Check for privacy. Do something more sane with the stacktrace
        #        or enable only when sending appropriate request arguments.
        if with_traceback:
            error_message += '\n' + last_error_and_traceback()
            log.error(error_message)
        bucket.request.setResponseCode(code)
        #bucket.request.setHeader('Content-Type', 'text/plain; charset=utf-8')
        return error_message.encode('utf-8')


class HttpDataFrameResponse(object):
    """
    Bottom layer of data forwarding workhorse for HTTP.

    Generate appropriate output content based on
    information in transformation data ``bucket.tdata``.

    Render pandas DataFrame to various tabular and hierarchical
    data formats and different timeseries plots.

    Tabular data:

        - CSV
        - JSON
        - HTML
        - Excel (XLSX)
        - DataTables HTML widget

    Hierarchical data:

        - HDF5
        - NetCDF

    Timeseries plots:

        - [PNG]  matplotlib
        - [PNG]  ggplot
        - [HTML] dygraphs
        - [HTML] Bokeh
        - [HTML] Vega/Vincent

    """

    def __init__(self, bucket, dataframe):
        self.bucket = bucket
        self.request = bucket.request
        self.dataframe = dataframe

    def render(self):
        """
        Evaluate ``bucket`` information and enrich further before
        executing the designated output format rendering handler.
        """

        # Variable aliases
        bucket = self.bucket
        df = self.dataframe

        # Read designated suffix from transformation data
        suffix = bucket.tdata.suffix.lower()

        # Update "time_begin" and "time_end" fields to be in ISO 8601 format
        tdata = deepcopy(bucket.tdata)
        tdata.update({
            'time_begin': slugify_datettime(bucket.tdata.time_begin),
            'time_end':   slugify_datettime(bucket.tdata.time_end),
        })

        # Compute some names and titles and pluck into ``bucket``
        bucket.title = Bunch(
            compact = u'{gateway}_{node}'.format(**dict(tdata)).replace('-', '_'),
            short = u'{network}_{gateway}_{node}'.format(**dict(tdata)).replace('-', '_'),
            full  = u'{network}_{gateway}_{node}_{time_begin}-{time_end}'.format(**dict(tdata)).replace('-', '_'),
            human = u'Address: {network} » {gateway} » {node}'.format(**dict(tdata)),
        )


        # Buffer object most output handlers write their content to
        buffer = BytesIO()


        # Dispatch to appropriate output handler
        # TODO: XML, SQL, GBQ (Google BigQuery table), MsgPack?, Thrift?
        # TODO: jsonline using Odo, see http://odo.pydata.org/en/latest/json.html
        # TODO: Refactor "if response: return response" cruft
        # TODO: Refactor dispatching logic to improve suffix comparison redundancy with UniversalTabularExporter

        if suffix in ['csv', 'txt']:
            # http://pandas.pydata.org/pandas-docs/stable/io.html#io-store-in-csv
            df.to_csv(buffer, header=True, index=False, date_format='%Y-%m-%dT%H:%M:%S.%fZ')

        elif suffix == 'tsv':
            df.to_csv(buffer, header=True, index=False, date_format='%Y-%m-%dT%H:%M:%S.%fZ', sep='\t')

        elif suffix == 'json':
            # http://pandas.pydata.org/pandas-docs/stable/io.html#io-json-writer
            df.to_json(buffer, orient='records', date_format='iso')

        elif suffix == 'html':
            # http://pandas.pydata.org/pandas-docs/stable/io.html#io-html
            df.to_html(buffer, index=False, justify='center')

        elif suffix == 'xlsx':
            exporter = UniversalTabularExporter(bucket, dataframe=df)
            response = exporter.render(suffix, buffer=buffer)
            if response:
                return response

        elif suffix in ['hdf', 'hdf5', 'h5']:
            exporter = UniversalTabularExporter(bucket, dataframe=df)
            response = exporter.render(suffix, buffer=buffer)
            if response:
                return response

        elif suffix in ['nc', 'cdf']:
            exporter = UniversalTabularExporter(bucket, dataframe=df)
            response = exporter.render(suffix, buffer=buffer)
            if response:
                return response

        elif suffix in ['dy', 'dygraphs']:
            plotter = UniversalPlotter(bucket, dataframe=df)
            response = plotter.render('html', kind='dygraphs')
            if response:
                return response

        elif suffix in ['dt', 'datatables']:
            exporter = UniversalTabularExporter(bucket, dataframe=df)
            response = exporter.render(suffix, buffer=buffer)
            if response:
                return response

        elif suffix in ['bk', 'bokeh']:
            plotter = UniversalPlotter(bucket, dataframe=df)
            response = plotter.render('html', kind='bokeh')
            if response:
                return response

        elif suffix == 'vega.json':
            plotter = UniversalPlotter(bucket, dataframe=df)
            response = plotter.render('json', kind='vega')
            if response:
                return response

        elif suffix == 'vega':
            plotter = UniversalPlotter(bucket, dataframe=df)
            response = plotter.render('html', kind='vega')
            if response:
                return response

        elif suffix in ['png']:
            plotter = UniversalPlotter(bucket, dataframe=df)
            response = plotter.render('png', buffer=buffer)
            if response:
                return response

        else:
            error_message = u'# Unknown data format "{suffix}"'.format(suffix=suffix)
            bucket.request.setResponseCode(http.BAD_REQUEST)
            bucket.request.setHeader('Content-Type', 'text/plain; charset=utf-8')
            return error_message.encode('utf-8')


        # Get hold of buffer content
        payload = buffer.getvalue()


        # Compute filename offered to browser
        filename = '{name}.{suffix}'.format(name=bucket.title.full, suffix=suffix)
        mimetype, encoding = mimetypes.guess_type(filename, strict=False)
        log.info(u'Fetching data succeeded, filename: {filename}, Format: {mimetype}', filename=filename, mimetype=mimetype)

        # Set "Content-Type" header
        if mimetype:
            bucket.request.setHeader('Content-Type', mimetype)

        # Set "Content-Disposition" header
        disposition = 'attachment'
        if mimetype in ['text/plain', 'text/csv', 'text/html', 'application/json', 'image/png']:
            disposition = 'inline'
        bucket.request.setHeader('Content-Disposition', '{disposition}; filename={filename}'.format(
            disposition=disposition, filename=filename))

        # Optionally encode to UTF-8 when serving HTML
        if mimetype == 'text/html':
            payload = payload.encode('utf-8')

        return payload

