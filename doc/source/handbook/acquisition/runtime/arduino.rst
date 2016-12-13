.. include:: ../../../_resources.rst

.. _daq-arduino:

#############################
Data acquisition with Arduino
#############################

.. todo:: Add complete example for Arduino.

.. _json-arduino:

*******************
Use JSON on Arduino
*******************
.. highlight:: cpp

`Arduino JSON library`_, an elegant and efficient JSON library for embedded systems::

    StaticJsonBuffer<200> jsonBuffer;

    JsonObject& root = jsonBuffer.createObject();

    // sensor name
    root["sensor"] = "gps";
    root["time"]   = 1351824120;

    JsonArray& data = root.createNestedArray("data");
    data.add(48.756080, 6);  // 6 is the number of decimals to use. default: 2
    data.add(2.302038, 6);

    root.printTo(Serial);
    // This prints:
    // {"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}

