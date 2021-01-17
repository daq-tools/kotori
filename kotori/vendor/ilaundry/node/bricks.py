# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from kotori.vendor.ilaundry.node.gpio import GpioInput, GpioOutput


class BinaryInputPort(object):

    def __init__(self, portname, signal=None):
        self.portname = portname
        self.signal = signal

        # detect edge on port
        self.gpio = GpioInput(self.portname, self.sensor_on)

    def sensor_on(self, port):
        print("DEBUG: Port {0} EVENT".format(self.portname))

        # signal sensor-on
        if self.signal:
            self.signal.set(True)

    # currently defunct
    """
    def sensor_off(self, port):
        print "SENSOR OFF:", port

        # signal sensor-off
        if self.callback:
            self.callback(False)
    """


class BinaryOutputPort(object):

    # TODO: handle different ports, not only GPIO

    #HIGH = 1
    #LOW = 2
    #BLINK = 3

    def __init__(self, portname):
        self.portname = portname
        #self.flavor = flavor or self.HIGH
        self.gpio = GpioOutput(self.portname)

        #self.modifier = modifier

    def set(self, *args, **kwargs):
        print("DEBUG: Port {0} ON".format(self.portname))
        self.gpio.on()

        # signal gpio port
        #if self.flavor == self.HIGH:
        #elif self.flavor == self.BLINK:

    def unset(self):
        print("DEBUG: Port {0} OFF".format(self.portname))

        #self.transition_stop()

        # signal gpio port
        self.gpio.off()


class Blinker(object):

    def __init__(self, port, interval=0.5):
        self.port = port
        self.interval = interval
        self.state = None
        self.transition = None

    def set(self, *args, **kwargs):
        self.blink()

    def unset(self):
        self.transition_stop()
        self.port.unset()

    def blink(self):
        self.transition_stop()
        self.transition = LoopingCall(self.blink_task)
        self.transition.start(self.interval)

    def transition_stop(self):
        if self.transition and self.transition.running:
            self.transition.stop()

    def blink_task(self):
        if self.state:
            self.state = False
            self.port.set()
        else:
            self.state = True
            self.port.unset()


class TimedBinarySemaphore(object):

    def __init__(self, holdtime=None, callback=None):
        self.holdtime = holdtime
        self.callback = callback
        self.timer = None

    def set(self, *args, **kwargs):
        #print "SEMAPHORE SET:  ", self.port

        # signal actor-on
        if self.callback:
            self.callback(True, *args, **kwargs)

        # start/reset timer for motion-off signal
        if self.holdtime:
            #print "SEMAPHORE SET:  ", self.port, "holding for {0} seconds".format(self.holdtime)
            if self.timer and not self.timer.called:
                self.timer.cancel()
            self.timer = reactor.callLater(self.holdtime, self.unset)

    def unset(self, *args, **kwargs):
        #print "SEMAPHORE UNSET:", self.port

        # signal sensor-off
        if self.callback:
            self.callback(False, *args, **kwargs)


class BinaryTopicSignal(object):
    """Receives a signal from bus network and signals receiver (actor/port) accordingly"""

    def __init__(self, bus, topic, signal):
        self.bus = bus
        self.topic = topic
        self.signal = signal
        self.bus.subscribe(self.topic, self.process_event)

    def process_event(self, topic, state):
        if state:
            self.signal.set()
        else:
            self.signal.unset()
