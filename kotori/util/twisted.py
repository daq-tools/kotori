# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas.motl@getkotori.org>
from __future__ import absolute_import
from twisted.logger import Logger
from twisted.internet.task import LoopingCall

log = Logger()


class SmartTask(object):

    def __init__(self, worker=None, interval=None, onerror='stop'):

        assert worker, 'The "worker" parameter is missing or None'
        assert interval, 'The "interval" parameter is missing or None'
        assert onerror in ['stop', 'restart'], 'Unknown value "{}" for parameter "onerror"'.format(onerror)

        self.worker = worker
        self.interval = interval
        self.onerror = onerror
        self.task = None

    def start(self, now=False):
        self.task = LoopingCall(self.worker)
        self.deferred = self.task.start(self.interval, now=now)
        self.deferred.addErrback(self.handle_error)

    def handle_error(self, failure, *args):
        log.failure('Task failed:\n{log_failure}', failure=failure)

        # Restart task after error
        if self.onerror == 'restart':
            self.start(now=False)
