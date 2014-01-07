# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.internet import reactor, task
from gpio import GpioInput, GpioOutput

class PirMotionDetector(object):

    def __init__(self, pir_port, signal_port, holdtime, callback):
        self.pir_port = pir_port
        self.signal_port = signal_port
        self.holdtime = holdtime
        self.callback = callback
        self.timer = None

        # detect edge on port
        pir = GpioInput(self.pir_port, self.motion_on)

    def motion_on(self, port):
        print "MOTION ON:", port

        # signal gpio port
        signal = GpioOutput(self.signal_port)
        signal.high()

        # signal motion-on
        self.callback(True)

        # start/reset timer for motion-off signal
        if self.timer and not self.timer.called:
            self.timer.cancel()
        self.timer = reactor.callLater(self.holdtime, self.motion_off, port)

    def motion_off(self, port):
        print "MOTION OFF:", port
        # signal motion-on
        self.callback(False)
