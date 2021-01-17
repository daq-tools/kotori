# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from pkg_resources import resource_filename
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from pyramid.paster import get_app


def boot_frontend(config, debug=False):
    """
    Boot a Pyramid WSGI application as Twisted component
    """

    http_port = int(config.get('config-web', 'http_port'))
    websocket_uri = str(config.get('wamp', 'listen'))

    # https://stackoverflow.com/questions/13122519/serving-pyramid-application-using-twistd/13138610#13138610
    config = resource_filename('kotori.frontend', 'development.ini')
    application = get_app(config, 'main')

    # https://twistedmatrix.com/documents/13.1.0/web/howto/web-in-60/wsgi.html
    resource = WSGIResource(reactor, reactor.getThreadPool(), application)

    reactor.listenTCP(http_port, Site(resource))
