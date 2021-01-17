# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas.motl@elmyra.de>
import math
import arrow
import datetime
from six import text_type
from dateutil.tz import gettz
from dateutil.parser import parse
from pyramid.settings import asbool
from twisted.web import http
from twisted.logger import Logger
from twisted.python.url import URL
from twisted.python.failure import Failure
from twisted.web.error import Error

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
            url = url.add(str(param), str(bucket.tdata[param]))

    for param, value in more_params.items():

        # Special rule: Don't add any of "pad" or "backfill", if "interpolate" is true
        do_interpolate = 'interpolate' in bucket.tdata and asbool(bucket.tdata.interpolate)
        if do_interpolate and param in ['pad', 'backfill']:
            continue

        url = url.add(str(param), str(value))

    data_uri = str(request.URLPath().sibling(sibling.encode()).click(url._to_bytes()))
    return data_uri


def twisted_honor_reverse_proxy(request):
    # Honor X-Forwarded-Proto request header if behind SSL-terminating HTTP proxy
    # See also: https://twistedmatrix.com/trac/ticket/5807
    hostname, port = twisted_hostname_port(request)
    is_ssl = twisted_is_secure(request)
    request.setHost(hostname.encode(), port, is_ssl)


def twisted_hostname_port(request):
    """
    Conveniently get (host, port) tuple of current request,
    either from "Host" header or from the request object itself.
    """
    host_header = request.getHeader('Host')
    if host_header:
        if ':' in host_header:
            hostname, port = host_header.split(':')
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
    for key, value in args.items():
        key = key.decode()
        result[key] = ','.join(map(lambda x: x.decode(), value))
    return result


def convert_floats(data, integers=None):
    """
    Convert all numeric values in dictionary to float type.
    """
    integers = integers or []
    delete_keys = []
    for key, value in data.items():
        try:
            if isinstance(value, datetime.datetime):
                continue
            if is_number(value):
                if key in integers:
                    data[key] = int(value)
                else:
                    data[key] = float(value)
            if math.isnan(data[key]):
                delete_keys.append(key)
        except:
            pass

    for key in delete_keys:
        del data[key]

    return data


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


def handleFailure(f, request=None):
    """
    Handle failure in callback chain, log and respond with traceback.

    See also:
    https://twistedmatrix.com/documents/16.0.0/core/howto/defer.html#errbacks
    """
    if f.type is Error:
        if request:
            request.setResponseCode(int(f.value.status))

        if hasattr(f.value, 'with_traceback'):
            f.with_traceback = f.value.with_traceback

        msg = None
        if isinstance(f.value.response, Failure):
            msg = f.value.response.getErrorMessage()
        elif type(f.value.response) in (str,):
            msg = f.value.response
        request.messages.append({'type': 'error', 'message': msg})

    else:
        if request:
            request.setResponseCode(http.INTERNAL_SERVER_ERROR)
            request.setHeader('Content-Type', 'text/plain; charset=utf-8')
        f.with_traceback = True

    if hasattr(f, 'with_traceback') and f.with_traceback:

        traceback = f.getTraceback()
        log.error(traceback)
        #f.trap(RuntimeError)
        request.write(traceback.encode('utf-8'))


def slugify_datettime(dstring):
    return arrow.get(dstring).to('utc').format('YYYYMMDDTHHmmss')


def parse_timestamp(timestamp):

    if isinstance(timestamp, text_type):

        # HACK: Assume CET (Europe/Berlin) for human readable timestamp w/o timezone offset
        qualified = any([token in timestamp for token in ['Z', '+', ' CET', ' CEST']])
        if not qualified:
            timestamp += ' CET'

        # Parse datetime string
        # Remark: Maybe use pandas.tseries.tools.parse_time_string?
        # TODO: Cache results of call to gettz to improve performance
        berlin = gettz('Europe/Berlin')
        tzinfos = {'CET': berlin, 'CEST': berlin}
        timestamp = parse(timestamp, tzinfos=tzinfos)

    return timestamp
