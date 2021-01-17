# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas.motl@elmyra.de>
from pyramid.predicates import RequestMethodPredicate
from pyramid.urldispatch import RoutesMapper
from pyramid.threadlocal import get_current_registry


class PathRoutingEngine(object):
    """
    A simple routing engine for path-based patterns
    based on the powerful Pyramid request router.
    """

    def __init__(self):
        self.mapper = RoutesMapper()

    def add_route(self, name, pattern, methods=None):
        methods = methods or []
        predicates = []
        for method in methods:
            predicate = RequestMethodPredicate(method.upper(), None)
            predicates.append(predicate)
        self.mapper.connect(name, pattern, predicates=predicates)

    def match(self, method, path):
        request = self._getRequest(attributes={'method': method}, environ={'PATH_INFO': path})
        result = self.mapper(request)
        if result['route']:
            return result

    def _getRequest(self, attributes, environ):
        # from pyramid.tests.test_urldispatch
        environ_default = {'SERVER_NAME': 'localhost',
                           'wsgi.url_scheme': 'http'}
        environ.update(environ_default)

        request = DummyRequest(attributes, environ)
        reg = get_current_registry()
        request.registry = reg
        return request


class DummyRequest(object):
    def __init__(self, attributes, environ):
        self.method  = None
        self.environ = environ
        for name, value in attributes.items():
            setattr(self, name, value)


if __name__ == '__main__':
    router = PathRoutingEngine()
    pattern = '/foo/bar/{resource}'
    router.add_route(pattern, pattern)
    print('match:   ', router.match('GET', '/foo/bar/entity-1'))
    print('mismatch:', router.match('GET', '/hello/world'))
