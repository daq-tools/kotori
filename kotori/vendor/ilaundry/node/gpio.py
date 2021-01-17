# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.internet import reactor
try:
    import Adafruit_BBIO.GPIO as GPIO
except Exception as ex:
    print("ERROR: No Adafruit_BBIO module installed:", ex)


class GpioInput(object):

    def __init__(self, port, callback):
        self.port = port
        self.callback = callback

        GPIO.setup(self.port, GPIO.IN)

        print("DETECT EVENTS:", self.port)

        # GPIO.RISING, GPIO.FALLING, GPIO.BOTH
        GPIO.remove_event_detect(self.port)
        GPIO.add_event_detect(self.port, GPIO.RISING, callback=self.check_rising, bouncetime=300)
        #GPIO.add_event_detect(self.port, GPIO.BOTH, callback=self.check_rising)
        #GPIO.add_event_detect(self.port, GPIO.FALLING, callback=self.check_falling)
        #GPIO.add_event_detect(self.port, GPIO.FALLING, self.check_falling)

    def check_rising(self, port):
        #print "check_rising:", port, self.port
        if port == self.port:
            reactor.callFromThread(self.callback, port)

    # doesn't work with Adafruit GPIO
    """
    def check_falling(self, port):
        if port == self.port:
            #self.callback(port)
            print "================= FALLING"
    """


class GpioOutput(object):

    def __init__(self, port):
        self.port = port
        GPIO.setup(self.port, GPIO.OUT)

    def on(self):
        self.high()

    def off(self):
        self.low()

    def low(self):
        GPIO.output(self.port, GPIO.LOW)

    def high(self):
        GPIO.output(self.port, GPIO.HIGH)
