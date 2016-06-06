# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import json
from urlparse import urlparse
from bunch import bunchify, Bunch
from twisted.application.service import Service
from twisted.internet import reactor
from twisted.logger import Logger
from twisted.web.resource import Resource
from twisted.web.server import Site
from kotori.io.router.path import PathRoutingEngine

log = Logger()

class HttpServerService(Service):

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

    def __init__(self):
        Resource.__init__(self)
        self.router    = PathRoutingEngine()
        self.endpoints = []
        self.callbacks = {}

    def registerEndpoint(self, path=None, callback=None):
        log.info('Registering endpoint at path {path}', path=path)
        if not callable(callback):
            log.error('Reference to endpoint {path} specified via "callback" '
                      'argument is not callable: {callback}', path=path, callback=callback)
            return

        endpoint = bunchify({'path': path, 'callback': callback})
        self.endpoints.append(endpoint)

        name = path
        self.router.add_route(name, path)
        self.callbacks[name] = callback

    def getChild(self, name, request):
        #log.info('getChild: {name}', name=name)
        uri = urlparse(str(request.URLPath()))

        # router v1
        """
        for endpoint in self.endpoints:
            if uri.path.startswith(endpoint.path):
                return HttpChannelEndpoint(options=endpoint)
        """

        # router v2
        result = self.router.match(uri.path)
        if result:
            route_name = result['route'].name
            callback = self.callbacks[route_name]
            endpoint = bunchify({'path': route_name, 'callback': callback, 'match': result['match']})
            return HttpChannelEndpoint(options=endpoint)

        return self


class HttpChannelEndpoint(Resource):

    isLeaf = True

    def __init__(self, options):
        self.options = options
        Resource.__init__(self)
        self.render_PUT = self.render_POST

    def render_POST(self, request):

        # Read and decode request
        content_type = request.getHeader('Content-Type')
        log.info('Received measurements via HTTP on uri {uri}, '
                 'content type is "{content_type}"', uri=request.path, content_type=content_type)

        body = request.content.read()
        if content_type.startswith('application/json'):
            payload = json.dumps(json.loads(body))

        elif content_type.startswith('application/x-www-form-urlencoded'):
            # TODO: Honor charset when receiving "application/x-www-form-urlencoded; charset=utf-8"
            data = tw_flatten_request_args(request.args)
            convert_floats(data)
            payload = json.dumps(data)

        else:
            log.warn('Unknown HTTP Content-Type {content_type}', content_type=content_type)
            return self.get_response(request.path, success=False)

        # Run forwarding callback
        outbound = Bunch(path=request.path, payload=payload, match=self.options['match'])
        self.options.callback(outbound)

        return self.get_response(request.path)

    def get_response(self, uri, success=True):
        if success:
            outcome = 'ACK'
        else:
            outcome = 'NACK'
        response = u'{outcome} "kotori-channel:/{uri}"'.format(uri=uri, outcome=outcome).encode('utf-8')
        return response

def tw_flatten_request_args(request_args):
    result = {}
    for key, value in request_args.iteritems():
        result[key] = ','.join(value)
    return result

def is_number(s):
    """
    http://pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def convert_floats(data):
    for key, value in data.iteritems():
        if is_number(value):
            value = float(value)
            data[key] = value

