# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from kotori.vendor.ilaundry.node.bricks import BinaryInputPort, BinaryOutputPort, TimedBinarySemaphore, Blinker, BinaryTopicSignal

PirMotionDetector = BinaryInputPort
PrivacyButton = BinaryInputPort
SignalLight = BinaryOutputPort
OperatorPresenceIndicator = BinaryTopicSignal


class FeatureBase(object):

    # port allocation
    PORT_LED = 'P8_13'
    PORT_PRIVACY_BUTTON = 'P8_15'
    PORT_PIR_SENSOR = 'P8_19'

    def __init__(self, node_id, bus, event_filters=None):
        self.node_id = node_id
        self.bus = bus
        self.event_filters = event_filters
        self.state = None

    @staticmethod
    def state_for_display(state):
        return state and 'enabled' or 'disabled'

    def run_filters(self, state):
        if self.event_filters:
            for event_filter in self.event_filters:
                state = event_filter(state)
        return state

    def publish(self, name, data):
        payload = {'node_id': self.node_id}
        payload.update(data)
        self.bus.publish(name, payload)


class ActivityMonitor(FeatureBase):

    def start(self, holdtime):
        """
        Feature for detecting activity of arbitrary creatures and reacting on that.

        - When triggered:
            - Turn LED into slow blinking mode
            - Publish "activity(True)" message to bus network
        - After "holdtime":
            - Turn LED off
            - Publish "activity(False)" message to bus network
        """

        # define a slow blinking light (default interval 0.5s)
        self.blinking_light = Blinker(SignalLight(self.PORT_LED))
        PirMotionDetector(self.PORT_PIR_SENSOR, signal=TimedBinarySemaphore(holdtime=holdtime, callback=self.on_event))

    def on_event(self, state, *args, **kwargs):

        if state == self.state: return
        self.state = state

        state = self.run_filters(state)

        print("INFO: Activity is", self.state_for_display(state))

        # turn led on/off
        if state:
            self.blinking_light.set()
        else:
            self.blinking_light.unset()

        # publish activity to bus network
        self.publish('broadcast:node-activity', {'state': state})


class PrivacyMonitor(FeatureBase):

    def start(self, holdtime):
        """
        Feature for disabling motion detection for some time, if user hits privacy button.

        - When triggered:
            - Turn LED on
            - Publish "privacy(True)" message to bus network
            - Store privacy state internally (for disabling "monitor_activity")
        - After "holdtime":
            - Turn LED off
            - Publish "privacy(False)" message to bus network
        """

        # define a basic light
        self.light = SignalLight(self.PORT_LED)
        PrivacyButton(self.PORT_PRIVACY_BUTTON, signal=TimedBinarySemaphore(holdtime=holdtime, callback=self.on_event))


    def on_event(self, state, *args, **kwargs):

        if state == self.state: return
        self.state = state

        state = self.run_filters(state)

        print("INFO: Privacy is", self.state_for_display(state))

        # turn led on/off and set/clear internal privacy state
        if state:
            self.light.set()
        else:
            self.light.unset()

        # publish privacy to bus network
        self.publish('broadcast:node-privacy', {'state': state})


class FeatureSet(FeatureBase):

    def __init__(self, node_id, bus):
        FeatureBase.__init__(self, node_id, bus)

        self.privacy_enabled = False

        self.privacy_monitor = PrivacyMonitor(self.node_id, self.bus, event_filters=[self.privacy_filter])
        self.activity_monitor = ActivityMonitor(self.node_id, self.bus, event_filters=[self.activity_filter])

        try:
            self.privacy_monitor.start(holdtime=60)
            self.activity_monitor.start(holdtime=5)
            self.show_operator_presence()
        except Exception as ex:
            print("ERROR: Feature start failed:", ex)


    def privacy_filter(self, state):
        self.privacy_enabled = state
        self.activity_monitor.on_event(False)
        return state

    def activity_filter(self, state):
        # skip further actions if privacy mode is enabled
        if state and self.privacy_enabled:
            print("INFO: Will signal no activity due to privacy mode being enabled")
            state = False
        return state

    def show_operator_presence(self):
        """
        Feature for showing whether there's an operator present.

        - When idle:
            - Listens to "broadcast:operator-presence" messages on bus network

        - When triggered:
            - True:  Turn LED into fast blinking mode
            - False: Turn LED off
        """

        # define a fast blinking light (default interval 0.1s)
        blinking_light = Blinker(SignalLight(self.PORT_LED), interval=0.1)

        # connect bus message to blinking light
        OperatorPresenceIndicator(self.bus, 'broadcast:operator-presence', blinking_light)
