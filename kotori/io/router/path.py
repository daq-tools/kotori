# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from pyramid.urldispatch import RoutesMapper
from pyramid.threadlocal import get_current_registry

class PathRoutingEngine(object):
    """
    A simple routing engine for path-based patterns
    based on the powerful Pyramid request router.
    """

    def __init__(self):
        self.mapper = RoutesMapper()

    def add_route(self, name, pattern):
        self.mapper.connect(name, pattern)

    def match(self, path):
        #print 'PathRoutingEngine attempt to match path:', path
        request = self._getRequest(PATH_INFO=path)
        result = self.mapper(request)
        if result['route']:
            #print 'PathRoutingEngine matched result:       ', result
            return result

    def _getRequest(self, **kw):
        # from pyramid.tests.test_urldispatch
        environ = {'SERVER_NAME':'localhost',
                   'wsgi.url_scheme':'http'}
        environ.update(kw)
        request = DummyRequest(environ)
        reg = get_current_registry()
        request.registry = reg
        return request

class DummyRequest(object):
    def __init__(self, environ):
        self.environ = environ


if __name__ == '__main__':
    router = PathRoutingEngine()
    pattern = '/foo/bar/{resource}'
    router.add_route(pattern, pattern)
    print 'match:   ', router.match('/foo/bar/entity-1')
    print 'mismatch:', router.match('/hello/world')

