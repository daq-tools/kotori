# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from string import Template
from pkg_resources import resource_filename
from twisted.logger import Logger
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File
from kotori.util.common import NodeId, get_hostname

log = Logger()


class CustomTemplate(Template):
    delimiter = '$$'


class WebDashboard(Resource):
    def getChild(self, name, request):
        print('getChild:', name)
        if name == '':
            return WebDashboardIndex()
        else:
            document_root = resource_filename('kotori.web', '')
            return File(document_root)


class WebDashboardIndex(Resource):

    def __init__(self, websocket_uri, filename):
        Resource.__init__(self)
        self.websocket_uri = websocket_uri
        self.filename = filename

    def render_GET(self, request):
        index = resource_filename('kotori.vendor.hydro2motion.web', self.filename)
        tpl = CustomTemplate(open(index).read())
        response = tpl.substitute({
            'websocket_uri': self.websocket_uri,
            'node_id': str(NodeId()),
            'hostname': get_hostname(),
        })
        return response.encode('utf-8')


def boot_web(settings, debug=False):

    http_port = int(settings.hydro2motion.http_port)
    websocket_uri = str(settings.wamp.uri)

    dashboard = Resource()
    dashboard.putChild('', WebDashboardIndex(websocket_uri=websocket_uri, filename='index.html'))
    dashboard.putChild('fs.html', WebDashboardIndex(websocket_uri=websocket_uri, filename='fs.html'))
    dashboard.putChild('poly.html', WebDashboardIndex(websocket_uri=websocket_uri, filename='poly.html'))
    dashboard.putChild('static', File(resource_filename('kotori.vendor.hydro2motion.web', 'static')))

    log.info('Starting HTTP service on port {http_port}', http_port=http_port)
    factory = Site(dashboard)
    reactor.listenTCP(http_port, factory)
