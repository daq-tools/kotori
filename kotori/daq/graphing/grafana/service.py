# -*- coding: utf-8 -*-
# (c) 2018-2021 Andreas Motl <andreas@getkotori.org>
from bunch import Bunch
from twisted.application.service import MultiService
from twisted.logger import Logger
from kotori.daq.services import MultiServiceMixin
from kotori.util.twisted import SmartTask

log = Logger()


class DashboardRefreshTamingService(MultiServiceMixin, MultiService):
    """
    Service for taming the refresh interval of Grafana dashboards.
    """

    def __init__(self, channel=None, preset='standard'):
        self.channel = channel or Bunch()
        self.preset = preset
        MultiService.__init__(self)

    def startService(self):
        self.setupService()
        self.log(log.info, u'Starting')

        # Start ourselves as Twisted Service
        MultiService.startService(self)

        # Start all worker tasks
        self.startTasks()

    def setupService(self):
        log.info(u'Setting up {name}', name=self.logname)
        #self.settings = self.parent.settings

    def startTasks(self):
        # Start tamer task
        try:
            self.tamer_start(now=True)
        except Exception as ex:
            log.failure('Starting dashboard refresh interval taming task failed: {ex}\n{log_failure}', ex=ex)

    def tamer_start(self, now=False):
        one_day = 60 * 60 * 24
        self.tamer = SmartTask(worker=self.tamer_process, interval=one_day, onerror='restart')
        self.tamer.start(now=now)

    def tamer_process(self):
        self.parent.tame_refresh_interval(preset=self.preset, force=False)
