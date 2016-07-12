# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl <andreas.motl@elmyra.de>
import arrow
from pyramid.settings import asbool
from twisted.web import http
from twisted.logger import Logger
from twisted.python.url import URL

log = Logger()

def get_data_uri(bucket, sibling=None, more_params=None):
    """
    Compute uri to data source as sibling to the current path.
    Add "from" and "to" query parameters from bucket.
    """

    more_params = more_params or {}

    forward_parameters = [u'from', u'to', u'exclude', u'include', u'pad', u'backfill', u'interpolate']

    request = bucket.request

    # Honor X-Forwarded-Proto request header if behind SSL-terminating HTTP proxy
    twisted_honor_reverse_proxy(request)

    url = URL()
    for param in forward_parameters:
        if param in bucket.tdata:
            url = url.add(unicode(param), unicode(bucket.tdata[param]))

    for param, value in more_params.iteritems():

        # Special rule: Don't add any of "pad" or "backfill", if "interpolate" is true
        do_interpolate = 'interpolate' in bucket.tdata and asbool(bucket.tdata.interpolate)
        if do_interpolate and param in ['pad', 'backfill']:
            continue

        url = url.add(unicode(param), unicode(value))

    data_uri = str(request.URLPath().sibling(sibling).click(url.asText()))
    return data_uri

def twisted_honor_reverse_proxy(request):
    # Honor X-Forwarded-Proto request header if behind SSL-terminating HTTP proxy
    # See also: https://twistedmatrix.com/trac/ticket/5807
    hostname, port = twisted_hostname_port(request)
    is_ssl = twisted_is_secure(request)
    request.setHost(hostname, port, is_ssl)

def twisted_hostname_port(request):
    """
    Conveniently get (host, port) tuple of current request,
    either from "Host" header or from the request object itself.
    """
    host_header = request.getHeader(b'Host')
    if host_header:
        if ':' in host_header:
            hostname, port = host_header.split(b':')
        else:
            is_ssl = twisted_is_secure(request)
            hostname, port = host_header, is_ssl and 443 or 80
    else:
        address = request.getHost()
        hostname, port = address.host, address.port

    return hostname, int(port)

def twisted_is_secure(request):
    return request.isSecure() or request.getHeader('X-Forwarded-Proto') == 'https'

def flatten_request_args(args):
    """
    Flatten Twisted request query parameters.
    """
    result = {}
    for key, value in args.iteritems():
        result[key] = ','.join(value)
    return result

def convert_floats(data):
    """
    Convert all numeric values in dictionary to float type.
    """
    for key, value in data.iteritems():
        if is_number(value):
            value = float(value)
            data[key] = value

def is_number(s):
    """
    Check string for being a numeric value.
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

def handleFailure(f, bucket=None):
    """
    Handle failure in callback chain, log and respond with traceback.

    See also:
    https://twistedmatrix.com/documents/16.0.0/core/howto/defer.html#errbacks
    """
    traceback = f.getTraceback()
    log.error(traceback)
    #f.trap(RuntimeError)
    if bucket:
        bucket.request.setResponseCode(http.INTERNAL_SERVER_ERROR)
        bucket.request.setHeader('Content-Type', 'text/plain; charset=utf-8')
    return traceback

def slugify_datettime(dstring):
    return arrow.get(dstring).to('utc').format('YYYYMMDDTHHmmss')

