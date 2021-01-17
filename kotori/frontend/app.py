# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from kotori.version import __VERSION__
from pyramid.config import Configurator


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""

    settings['SOFTWARE_VERSION'] = __VERSION__

    config = Configurator(settings=settings)

    # Addons
    config.include('pyramid_jinja2')
    # http://docs.pylonsproject.org/projects/pyramid-jinja2/en/latest/#adding-or-overriding-a-renderer
    config.add_jinja2_renderer('.html')
    config.include('cornice')

    # Views and routes
    config.add_static_view('static/app', 'static/app', cache_max_age=0)
    config.add_static_view('static/lib', 'static/lib', cache_max_age=60 * 24)
    config.add_route('index', '/')

    config.scan()

    return config.make_wsgi_app()
