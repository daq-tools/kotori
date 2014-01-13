# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from string import Template
from pkg_resources import resource_filename
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File
from ilaundry.util import NodeId


class CustomTemplate(Template):
    delimiter = '$$'

class WebDashboard(Resource):
    def getChild(self, name, request):
        print 'getChild:', name
        if name == '':
            return WebDashboardIndex()
        else:
            document_root = resource_filename('ilaundry.web', '')
            return File(document_root)

class WebDashboardIndex(Resource):

    def __init__(self, websocket_uri):
        Resource.__init__(self)
        self.websocket_uri = websocket_uri

    def render_GET(self, request):
        index = resource_filename('ilaundry.web', 'index.html')
        tpl = CustomTemplate(file(index).read())
        response = tpl.substitute({'websocket_uri': self.websocket_uri, 'node_id': str(NodeId())})
        return response

def boot_web(http_port, websocket_uri, debug=False):

    dashboard = Resource()
    dashboard.putChild('', WebDashboardIndex(websocket_uri=websocket_uri))
    dashboard.putChild('static', File(resource_filename('ilaundry.web', 'static')))

    print 'INFO: Starting HTTP service on port', http_port
    factory = Site(dashboard)
    reactor.listenTCP(http_port, factory)


