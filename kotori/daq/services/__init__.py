# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.application.service import MultiService

class MultiServiceMixin(object):

    def __init__(self, name=None):
        MultiService.__init__(self)
        self.name = name

    def startService(self):
        try:
            self.setupService()
        except AttributeError:
            pass
        MultiService.startService(self)

    def registerService(self, service):
        service.setServiceParent(self)

    @property
    def logname(self):
        return u'{class_name}({name})'.format(class_name=self.__class__.__name__, name=self.name)

class RootService(MultiService, MultiServiceMixin):

    def __init__(self, settings=None):
        MultiService.__init__(self)
        self.settings = settings

    def makeService(self, service_class, *args, **kwargs):
        service = service_class(*args, **kwargs)
        self.registerService(service)
        return service

