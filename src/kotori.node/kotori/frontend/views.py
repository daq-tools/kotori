# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import logging
from pkg_resources import resource_filename
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response, FileResponse
from pyramid.url import route_path
from pyramid.view import view_config

log = logging.getLogger(__name__)

def includeme(config):

    # serve favicon.ico
    # http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/assets.html#registering-a-view-callable-to-serve-a-static-asset
    config.add_route('favicon', 'favicon.ico')
    config.add_view('kotori.frontend.views.favicon_view', route_name='favicon')


@view_config(route_name='index', renderer='kotori.frontend:templates/index.html')
def index_page(request):
    software_version = request.registry.settings['SOFTWARE_VERSION']
    tplvars = {
        'software_version': software_version,
    }
    return tplvars


def favicon_view(request):
    """
    http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/assets.html#registering-a-view-callable-to-serve-a-static-asset
    """
    icon = resource_filename('kotori.frontend', 'static/favicon.ico')
    if os.path.isfile(icon):
        return FileResponse(icon, request=request)
    else:
        return HTTPNotFound()
