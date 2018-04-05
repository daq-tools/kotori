# -*- coding: utf-8 -*-
"""Implementation of a Twisted-friendly thread pool wrapper."""
from __future__ import absolute_import
from functools import partial
from twisted.internet.threads import deferToThreadPool
from twisted.internet.defer import fail
from twisted.internet.error import ReactorNotRunning

# Shamelessly stolen from:
# https://github.com/lvh/thimble
# https://pypi.python.org/pypi/thimble

class Thimble(object):

    """A Twisted thread-pool wrapper for a blocking API."""

    def __init__(self, reactor, pool, wrapped, blocking_methods):
        """Initialize a :class:`Thimble`.
        :param reactor: The reactor that will handle events.
        :type reactor: :class:`twisted.internet.interfaces.IReactorThreads` and
            :class:`twisted.internet.interfaces.IReactorCore`. Pretty much any
            real reactor implementation will do.
        :param pool: The thread pool to defer to.
        :type pool: :class:`twisted.python.threadpool.ThreadPool`
        :param wrapped: The blocking implementation being wrapped.
        :param blocking_methods: The names of the methods that will be wrapped
            and executed in the thread pool.
        :type blocking_methods: ``list`` of native ``str``
        """
        self._reactor = reactor
        self._pool = pool
        self._wrapped = wrapped
        self._blocking_methods = blocking_methods

    def _deferToThreadPool(self, f, *args, **kwargs):
        """Defer execution of ``f(*args, **kwargs)`` to the thread pool.
        This returns a deferred which will callback with the result of
        that expression, or errback with a failure wrapping the raised
        exception.
        """
        if self._pool.joined:
            return fail(
                ReactorNotRunning("This thimble's threadpool already stopped.")
            )
        if not self._pool.started:
            self._pool.start()
            self._reactor.addSystemEventTrigger(
                'during', 'shutdown', self._pool.stop)

        return deferToThreadPool(self._reactor, self._pool, f, *args, **kwargs)

    def __getattr__(self, attr):
        """Get and maybe wraps an attribute from the wrapped object.
        If the attribute is blocking, it will be wrapped so that
        calling it will return a Deferred and the actual function will
        be ran in a thread pool.
        """
        value = getattr(self._wrapped, attr)

        if attr in self._blocking_methods:
            value = partial(self._deferToThreadPool, value)

        return value
