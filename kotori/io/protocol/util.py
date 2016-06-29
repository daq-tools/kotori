# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl <andreas.motl@elmyra.de>
import arrow
from twisted.web import http
from twisted.logger import Logger
from twisted.python.url import URL

log = Logger()

def get_data_uri(bucket, sibling=None):
    """
    Compute uri to data source as sibling to the current path.
    Add "from" and "to" query parameters from bucket.
    """
    url = URL()
    if 'from' in bucket.tdata:
        url = url.add(u'from', unicode(bucket.tdata['from']))
    if 'to' in bucket.tdata:
        url = url.add(u'to', unicode(bucket.tdata['to']))
    data_uri = str(bucket.request.URLPath().sibling(sibling).click(url.asText()))
    return data_uri

def twisted_flatten_request_args(request):
    """
    Flatten Twisted request query parameters.
    """
    result = {}
    for key, value in request.args.iteritems():
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

