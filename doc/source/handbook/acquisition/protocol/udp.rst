.. include:: ../../../_resources.rst

.. _daq-udp:

#########################
Data acquisition over UDP
#########################

.. seealso:: :ref:`vendor-hydro2motion`
.. seealso:: :ref:`vendor-lst`

UDP over DTN
============
Proposal::

    echo '## time,Gewicht,Aussen-Temperatur,Aussen-Feuchtigkeit,Spannung' | socat -i dtn0 - udp:offgrid.local:5001

.. hint:: Not implemented yet.

