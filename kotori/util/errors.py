# -*- coding: utf-8 -*-
# (c) 2014-2021 Andreas Motl, <andreas@getkotori.org>
import sys
import traceback
from io import StringIO


def traceback_get_exception(num = -1):

    # Build error message.
    exc_info = sys.exc_info()
    exception_string = ''.join(traceback.format_exception_only(exc_info[0], exc_info[1]))

    # Extract error details from traceback.
    try:
        (filename, line_number, function_name, text) = traceback.extract_tb(exc_info[2])[num]
    except:
        (filename, line_number, function_name, text) = ('-', '-', '-', '-')

    error = {
        'message': exception_string,
        'location': {
            'filename': filename,
            'line_number': line_number,
            'function_name': function_name,
            'text': text,
            }
    }

    return error


def format_exception_location(error, prefix=''):
    if prefix:
        prefix += "\n"
    error_location =\
    prefix +\
    "Filename:    %s\nLine number: %s\nFunction:    %s\nCode:        %s" %\
    (error['location']['filename'], error['location']['line_number'], error['location']['function_name'], error['location']['text'])
    return error_location


def last_error_and_traceback():
    error_entry = traceback_get_exception(0)
    error_last = traceback_get_exception(-1)
    sep = '-' * 60
    payload_location = "\n".join([sep, format_exception_location(error_entry, "Entry point:"), sep, format_exception_location(error_last, "Source of exception:")])
    payload = ''.join(["ERROR: ", error_entry['message'], "\n", payload_location, "\n"])

    # add full traceback
    buffer = StringIO()
    traceback.print_exc(file=buffer)
    buffer.seek(0)
    payload += '\n' + buffer.read()

    return payload
