.. include:: ../_resources.rst

.. _decoder-gps-logger-for-android:

#####################
GPSLogger for Android
#####################

.. contents::
   :local:
   :depth: 1

----


*****
About
*****
The `GPSLogger for Android`_ is a battery-efficient GPS logging application.

GPSLogger uses the GPS capabilities of your Android phone to log coordinates
to GPS format files at regular intervals. This can be particularly useful if
you want to geotag your photos after a day out or share your travel route
with someone. The purpose of this application is to be battery efficient
to save you battery power when abroad and last as long as possible.


Custom URL feature
==================
By `using the Custom URL feature`_, GPS information can be logged to Kotori
efficiently and for as many users as desired.

The Custom URL feature allows you to log GPS points to a public URL.
This can be a third party API that accepts GET requests or an application
that you've written and are hosting on your own server.

If you check the 'POST' checkbox, then the querystring parameters are sent
in the HTTP POST body.

If your phone goes offline, then the app will queue these requests until a
data connection becomes available.

The URL pattern can be defined like::

    https://gpslogger.example.org/log?latitude=%lat&longitude=%lon...

Please have a look at implementation of the `GPSLogger url parameters`_ for
reviewing all available url parameters.

.. figure:: https://gpslogger.app/images/gps_icon05.png
    :target: https://gpslogger.app/images/gps_icon05.png
    :alt: GPSLogger for Android Logo
    :width: 300px

    GPSLogger for Android

.. _GPSLogger for Android: https://gpslogger.app/
.. _using the Custom URL feature: https://gpslogger.app/#usingthecustomurlfeature
.. _GPSLogger url parameters: https://github.com/mendhak/gpslogger/blob/v102/gpslogger/src/main/java/com/mendhak/gpslogger/loggers/customurl/CustomUrlLogger.java#L89-L120


*************
Configuration
*************
The API URL should look like::

    https://daq.example.org/api/{realm}/{owner}/{group}/{device}/gpslogger

A meaningful example instance would be::

    https://daq.example.org/api/gpstrack/3ED60B81-3957-49F0-B148-50196CD6A226/default/android-one/gpslogger

Currently, Kotori does not employ any authentication on its HTTP interface.
In the meanwhile, you might want to configure that on a Nginx reverse proxy
you might be running in front of Kotori anyway.
