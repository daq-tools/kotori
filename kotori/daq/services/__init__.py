# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.application.service import MultiService

class RootService(MultiService):

    def __init__(self, settings=None):
        MultiService.__init__(self)
        self.settings = settings

    def makeService(self, service_class, *args, **kwargs):
        service = service_class(*args, **kwargs)
        self.registerService(service)
        return service

    def registerService(self, service):
        service.setServiceParent(self)
