:orphan:

.. include:: ../_resources.rst

.. _vendor-ilaundry:

########
iLaundry
########

.. contents:: Table of Contents
   :local:
   :depth: 1


*****
About
*****
This integrates the GPIO ports of a `BeagleBone Black`_ (BBB) SoC machine
using the ``Adafruit_BBIO`` library with a distributed node environment based on WAMP_.

For wiring things together, it sports a highlevel API based on components written in Python.
We have *bricks* as the core building blocks and *features* on top of them.

This was made in 2014, today you might want to have a look at things like `Node-RED`_,
which might be able to achieve similar things but also sports a rich ecosystem of addons
called `Node-RED flows`_ and a visual editor for connecting these components to each other.

ScratchX_ might offer the same infrastructure through `ScratchX Wiki`_/`Scratch Extensions`_, let's check:

    [...] make it possible to connect Scratch projects with external hardware (such as LEGO WeDo or PicoBoard)
    or sources of information on the web. They add a collection of command and reporter blocks that can be used
    to interact with a particular device or data source. When an extension is enabled, its blocks appear in
    the "More Blocks" palette.

`Snap!`_ is also supported by the `Scratch 2 Offline Editor Hardware Extension for Arduino`_.

Also take a look at Xideco_, a network-enabled software backplane in form of a cross-platform
interconnect fabric between the popular Arduino, Raspberry and BeagleBone Black platforms.
Read their `Intro to Xideco`_.

.. seealso::
    For an introduction to BBB GPIO programming using Python,
    have a look at the tutorial `Using the Adafruit_BBIO Library`_.

Bricks
======
- BinaryInputPort: Monitor a GPIO input port, emit signals on state changes
- BinaryOutputPort: Set or unset a GPIO output port
- Blinker: Toggle GPIO output port between on and off
- TimedBinarySemaphore: Building block for a virtual push-button

    - set a GPIO output port
    - hold it for a configurable ``holdtime``
    - unset the GPIO output port

- BinaryTopicSignal

    - Receive a signal from a bus network and forward to receiver actor/port.


Features
========
On top of these *bricks*, *features* can be implemented.


ActivityMonitor
---------------
Let's implement a *feature* for detecting motion using a PIR sensor
connected to a GPIO port and reacting on that. It should:

- When PIR sensor was triggered through some activity:

    - Turn LED into slow blinking mode
    - Publish "activity(True)" message to bus network

- After "holdtime":

    - Turn LED off
    - Publish "activity(False)" message to bus network

The implementation of this feature is almost pseudo code based on composition of components::

    # Define some aliases for bricks. Naming things.
    PirMotionDetector = BinaryInputPort
    SignalLight       = BinaryOutputPort

    class ActivityMonitor(FeatureBase):

        # port allocation
        PORT_LED = 'P8_13'
        PORT_PIR_SENSOR = 'P8_19'

        def start(self, holdtime):

            # Define a slow blinking light (default interval 0.5s)
            self.blinking_light = Blinker(SignalLight(self.PORT_LED))

            # Define a PIR data source and connect it to the slow blinking light
            PirMotionDetector(self.PORT_PIR_SENSOR, signal=TimedBinarySemaphore(holdtime=holdtime, callback=self.on_event))

        def on_event(self, state, *args, **kwargs):

            # Turn led on or off based on output state of a component
            if state:
                self.blinking_light.set()
            else:
                self.blinking_light.unset()

            # Publish activity to bus network forwarding the current state of the component
            self.publish('broadcast:node-activity', {'state': state})



*******
Details
*******

.. attention::

    This section is just a stub. Read the source, luke.

Embedded use
============

Setup node sandbox
------------------
::

    apt-get install mplayer

    python -m venv .venv
    source .venv/bin/activate
    pip install distribute==0.6.45
    pip install Adafruit_BBIO

    cd src/kotori.node
    python setup.py develop
    cd -


Master/node modes
=================

master only::

    kotori master --debug

node only::

    kotori node --master=ws://offgrid:9000/ws --debug
    kotori node --master=ws://beaglebone.local:9000/ws --debug
    kotori node --master=ws://master.example.com:9000/ws --debug

