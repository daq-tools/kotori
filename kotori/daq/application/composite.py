# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from bunch import Bunch
from twisted.logger import Logger
from kotori import KotoriBootloader
from kotori.configuration import read_list
from kotori.daq.services import RootService

log = Logger()

class CompositeApplication(RootService):
    """
    Application service container root object
    """

    def __init__(self, name=None, application_settings=None, global_settings=None):
        RootService.__init__(self, settings=global_settings)

        # Compute name for Twisted service
        self.name = u'app-{name}'.format(name=name)

        # Make channel object from application settings configuration object
        self.channel = Bunch(**application_settings)

        # Main application components
        for service_reference in read_list(application_settings.services):

            # Load service component
            service_factory = KotoriBootloader.load_entrypoint(service_reference)

            # Load data processing strategy and graphing components
            # TODO: Review whether this should be per-service or not
            strategy_factory = KotoriBootloader.load_entrypoint(application_settings.strategy)
            graphing_factory = KotoriBootloader.load_entrypoint(application_settings.graphing)

            # Create application service object composed of subsystem components
            # TODO: Bundle all arguments into yet another wrapper object for an universal object factory
            service = service_factory(
                channel  = self.channel,
                strategy = strategy_factory(settings=global_settings),
                graphing = graphing_factory(settings=global_settings)
                )

            # Register service component with its container
            self.registerService(service)


def boot(name=None, **kwargs):
    # Bootstrap application composed of components defined by configuration settings
    app = CompositeApplication(name=name, **kwargs)
    return app
