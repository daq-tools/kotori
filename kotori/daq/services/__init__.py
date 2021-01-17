# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl <andreas@getkotori.org>
from copy import deepcopy

from bunch import Bunch
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

    def setupChannel(self, channel=None, name=None):
        """
        Make channel object from application settings configuration object
        """

        assert channel is not None, 'Channel object must not be None'

        channel = deepcopy(channel)
        if name:
            channel.update(name=name)
        self.channel = Bunch(**channel)

    @property
    def logname(self):
        return u'{class_name}({name})'.format(class_name=self.__class__.__name__, name=self.name)

    def log(self, level, prefix):
        level('{prefix} {class_name}. name={name}, channel={channel}',
            prefix=prefix, class_name=self.__class__.__name__, name=self.name, channel=dict(self.channel))


class RootService(MultiService, MultiServiceMixin):

    def __init__(self, settings=None):
        MultiService.__init__(self)
        self.settings = settings

    def makeService(self, service_class, *args, **kwargs):
        service = service_class(*args, **kwargs)
        self.registerService(service)
        return service
