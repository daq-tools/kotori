# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl <andreas.motl@elmyra.de>
import json
import types
import mimetypes
from six import BytesIO
from copy import deepcopy
from urlparse import urlparse
from bunch import bunchify, Bunch
from twisted.application.service import Service
from twisted.internet import reactor
from twisted.logger import Logger
from twisted.web import http
from twisted.web.http import parse_qs
from twisted.web.resource import Resource
from twisted.web.server import Site
from kotori.io.router.path import PathRoutingEngine
from kotori.io.export.tabular import UniversalTabularExporter
from kotori.io.export.plot import UniversalPlotter
from kotori.io.protocol.util import convert_floats, slugify_datettime, flatten_request_args
from kotori.errors import last_error_and_traceback

log = Logger()

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
        factory = Site(self.root)
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
        self.router    = PathRoutingEngine()
        self.callbacks = {}

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
            return HttpChannelEndpoint(options=endpoint)

        # If nothing matched, continue traversal
        return self


class HttpChannelEndpoint(Resource):
    """
    Upper layer of data forwarding workhorse for HTTP.

    Twisted Site HTTP leaf resource containing the main dispatcher
    logic for forwarding inbound requests to the routing target.
    """

    isLeaf = True

    def __init__(self, options):
        self.options = options
        Resource.__init__(self)

    def render(self, request):
        """
        Main Twisted Resource rendering method,
        overridden to provide custom logic.
        """

        # Pluck ``error_response`` method to request object
        request.error_response = self.error_response

        # Dispatch request to target service
        return self.dispatch(request)

    def dispatch(self, request):
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

        content_type = request.getHeader('Content-Type')
        log.info('Received HTTP request on uri {uri}, '
                 'content type is "{content_type}"', uri=request.path, content_type=content_type)

        # Read and decode request body
        data = Bunch()
        body = request.content.read()
        if body:
            if content_type.startswith('application/json'):
                data = json.loads(body)

            elif content_type.startswith('application/x-www-form-urlencoded'):
                # TODO: Honor charset when receiving "application/x-www-form-urlencoded; charset=utf-8"
                data = parse_qs(body, 1)

            else:
                log.warn('Unknown HTTP Content-Type {content_type}', content_type=content_type)
                return self.get_response(request.path, success=False)

            # TODO: Apply this to telemetry values only!
            # FIXME: This is a hack
            if 'firmware' not in self.options.path:
                convert_floats(data)

        # Main transformation data container
        tdata = Bunch()

        # Merge request parameters (GET and POST) and url matches, in this order
        tdata.update(flatten_request_args(request.args))
        tdata.update(self.options.match)

        # Serialize as json for convenience
        # TODO: Really?
        data_json = json.dumps(data)

        # Main bucket data container object serving the whole downstream processing chain
        bucket = Bunch(path=request.path, data=data, json=data_json, tdata=tdata, request=request, body=body)

        # Run forwarding callback
        response = self.options.callback(bucket)

        # FIXME: This is nasty
        # NOT_DONE_YET = 1 (types.IntType)
        if isinstance(response, (bytes, types.IntType)):
            return response
        else:
            return self.get_response(request.path)

    def get_response(self, uri, success=True):
        """
        Default HTTP response method. Currently used for acknowledging inbound telemetry data.
        """
        # TODO: Improve this, only use in the appropriate context.
        if success:
            outcome = 'ACK'
        else:
            outcome = 'NACK'
        response = u'{outcome} "kotori-channel:/{uri}"'.format(uri=uri, outcome=outcome).encode('utf-8')
        return response

    @staticmethod
    def error_response(bucket, error_message='', with_traceback=False):
        """
        Error handling method logging and returning appropriate stacktrace.
        """
        # FIXME: Check for privacy. Do something more sane with the stacktrace
        #        or enable only when sending appropriate request arguments.
        if with_traceback:
            error_message += '\n' + last_error_and_traceback()
            log.error(error_message)
        bucket.request.setResponseCode(http.BAD_REQUEST)
        bucket.request.setHeader('Content-Type', 'text/plain; charset=utf-8')
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
            df.to_csv(buffer, index=False)

        elif suffix == 'json':
            # http://pandas.pydata.org/pandas-docs/stable/io.html#io-json-writer
            df.to_json(buffer, orient='records')

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

