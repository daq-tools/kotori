================
iLaundry CHANGES
================

develop
-------


2014-01-21 0.1.0
----------------
- node: reactivate heartbeat
- node: mplayer user-agent hack for correctly spelling umlauts
- ui: indicate motion activity from node
- ui: indicate node online/offline state
- ui: indicate privacy mode
- ui: button for toggling operator presence
- ether: refactored node registration, send hostname along
- ui: layout refactoring, display more details


2014-01-13 0.0.4
----------------
- ui: introduce Bootstrap, jQuery, underscore, etc.
- ui: reflect multinode capabilities


2014-01-13 0.0.3
----------------
- modularized into three components: master, node, web
- single-daemon mode
- first feature set on top of Adafruit_BBIO.GPIO


2014-01-05 0.0.2
----------------
- Multiple nodes for real [NodeRegistry]


2014-01-05 0.0.1
----------------
proof-of-concept

- Two daemons: master service and node service
- Communication infrastructure on top of Autobahn using PubSub
- Text-to-speech on top of Google Translate TTS
- Basic HTML Dashboard GUI for sending text messages
