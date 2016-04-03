from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

#from kotori.daq.intercom.mqtt.twisted import TwistedMqttAdapter
#MqttAdapter = TwistedMqttAdapter

from kotori.daq.intercom.mqtt.paho import PahoMqttAdapter
MqttAdapter = PahoMqttAdapter
