================
kotori-mqtt TODO
================

Prio 1
======
- [x] node registration: send hostname along
- [o] node_id-to-label translator with server-side persistence at master node
- [o] run as init.d daemon

Prio 2
======
- [o] show embedded video when node signals activity
- [o] Bug when speaking umlauts, like "Bolognesääää!"::

    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150] Traceback (most recent call last):
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]   File ".venv27/local/lib/python2.7/site-packages/autobahn-0.7.0-py2.7.egg/autobahn/wamp.py", line 863, in onMessage
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]     self.factory.dispatch(topicUri, event, exclude, eligible)
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]   File ".venv27/local/lib/python2.7/site-packages/autobahn-0.7.0-py2.7.egg/autobahn/wamp.py", line 1033, in dispatch
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]     log.msg("publish event %s for topicUri %s" % (str(event), topicUri))
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150] UnicodeEncodeError: 'ascii' codec can't encode characters in position 8-12: ordinal not in range(128)

Prio 3
======
- [o] send dates in messages
- [o] notifications: Pushover- and SMS-integration
