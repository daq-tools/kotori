##############
Kotori Box DIY
##############

*********
Main unit
*********

Raspberry Pi 3 Model B
======================

- | Pollin 94-702850
  | http://www.pollin.de/shop/dt/OTQxNzkyOTk-/Bausaetze_Module/Entwicklerboards/Raspberry_PI/Raspberry_Pi_3_Modell_B.html

- | Pollin 94-723625
  | http://www.pollin.de/shop/dt/NDczNjcyOTk-/Computer_und_Zubehoer/Hardware/Speicherkarten/microSDHC_Card_KINGSTON_SDCA10_UHS_I_10_16_GB_Class_10.html


************
Power Supply
************
Power is important.

Grid
====
- | Pollin 94-351537
  | http://www.pollin.de/shop/dt/MjY0ODQ2OTk-/Stromversorgung/Netzgeraete/Steckernetzgeraete/Steckernetzteil_QUATPOWER_PSN5_2000M_5_V_2_A_Micro_USB.html

Mobile
======
- | Pollin 94-351235
  | http://www.pollin.de/shop/dt/NDY3ODQ2OTk-/Stromversorgung/Akkus/Powerbanks_Zusatzakkus/USB_Powerbank_LiPo_6000_mAh.html

- | Pollin 94-351771
  | http://www.pollin.de/shop/dt/ODIyODQ2OTk-/Stromversorgung/Ladegeraete/USB_Ladegeraete/Universal_Solar_Ladeset_Logilink_PA0025_B_Ware.html

- | Pollin 94-271384
  | http://www.pollin.de/shop/dt/NTE2ODI3OTk-/Stromversorgung/Akkus/LiPo_Akkus/LiPo_Akkupack_BAK_293450_3_7_V_450_mAh.html

Micro UPS
=========

- ATXRaspi

    - http://lowpowerlab.com/atxraspi/
    - http://lowpowerlab.com/blog/2015/03/09/new-atxraspi-reboot-function/
    - https://www.youtube.com/watch?v=w4vSTq2WhN8
    - https://lowpowerlab.com/forum/index.php/topic,17.msg22.html
    - http://www.nin10doshop.com/webshop/diy---kits--parts/detail/30/atx-raspi-board.html

- Mightyboost

    - http://lowpowerlab.com/mightyboost/
    - https://lowpowerlab.com/shop/mightyboost

- PiUSV

    - http://www.piusv.de/
    - http://piusv.de/forum/
    - `<http://www.pollin.de/shop/dt/ODkzNzkyOTk-/Bausaetze_Module/Entwicklerboards/Raspberry_PI/Raspberry_Pi_USV_CW2_PiUSV_.html>`_


************
DAQ adapters
************

Wired
=====
- LabJack U3-HV

    - https://labjack.com/products/u3
    - https://labjack.com/accessories/cb15-terminal-board
    - https://www.reichelt.de/LABJACK-U3-HV/3/index.html?&ACTION=3&LA=446&ARTICLE=131924&artnr=LABJACK+U3+HV
    - https://www.reichelt.de/LABJACK-U3-LV/3/index.html?&ACTION=3&LA=446&ARTICLE=131925&artnr=LABJACK+U3+LV
    - http://www.meilhaus.de/en/labjack-u3,i53.htm

Wireless
========

RF69
----
- | JeeLink (v3c)
  | ATmega328p with RFM69CW and USB interface
  | http://jeelabs.net/projects/hardware/wiki/JeeLink#JeeLink-v3c
  | http://www.digitalsmarties.net/products/jeelink

IEEE 802.15.4
-------------
Access 6LoWPAN and ZigBee

- USB, CC2531 based: http://de.aliexpress.com/wholesale?catId=0&initiative_id=&SearchText=CC2531+USB
- http://openlabs.co/OSHW/Raspberry-Pi-802.15.4-radio
- http://openlabs.co/store/Raspberry-Pi-802.15.4-radio
- http://busware.de/tiki-index.php?page=RF212USB
- http://www.atmel.com/devices/AT86RF212B-ZigBit-Wireless-Module.aspx
- http://www.atmel.com/images/doc8168.pdf

ZWave
-----
- http://shop.busware.de/product_info.php/products_id/29
- http://shop.busware.de/product_info.php/products_id/44

LoRa
----
- | iU880A - Long Range USB Adapter
  | http://www.wireless-solutions.de/products/gateways/iu880a-usb
  | http://webshop.imst.de/iu880a-long-range-usb-adapter.html

- | MK002-xx-EU – USB Key
  | http://www.nemeus.fr/en/mk002-usb-key/



************
Connectivity
************

WiFi
====
A second WiFi might be handy:
The onboard WiFi provides an access point for receiving ingress telemetry data,
while the other one might optionally connect to an upstream internet gateway.

3G/4G
=====
Connect to the internet using a GPRS_/UMTS_/LTE_ uplink.


*******
Housing
*******

- | Pollin 94-702352
  | http://www.pollin.de/shop/dt/NzQ2NzkyOTk-/Bausaetze_Module/Entwicklerboards/Raspberry_PI/Raspberry_Pi_B_Gehaeuse_TEKO_TEK_BERRY_9_schwarz.html

- | ABS-76Z Hermetisches Universalgehäuse ABS 120x70x40 verschraubbar
  | http://rf-store.com/index.php?view=2&pv=showart&prod_id=ABS-76Z


********
Software
********

Raspbian
========

Command line installer
----------------------

https://www.raspberrypi.org/downloads/raspbian/
::

    wget https://downloads.raspberrypi.org/raspbian_lite_latest
    unzip 2016-05-10-raspbian-jessie-lite.zip

https://www.raspberrypi.org/documentation/installation/installing-images/README.md

- Identify the SD card disk::

    diskutil list

- Unmount your SD card by using the disk identifier, to prepare for copying data to it::

    diskutil unmountDisk /dev/disk1

- Copy the data to your SD card::

    sudo dd bs=1M if=~/Downloads/2016-05-10-raspbian-jessie-lite.img of=/dev/rdisk1

- Eject the card::

    sudo diskutil unmountDisk /dev/disk1
    sudo diskutil eject /dev/rdisk1


User interface installers
-------------------------
See also https://www.raspbian.org/RaspbianInstaller


Boot RaspberryPi
================
- Insert SD Card into slot, connect with Ethernet and power up the system
- Login::

    # The default password for user "pi" is "raspberry"
    ssh pi@raspberrypi

    sudo su -

.. note:: You should change your default password, see https://www.raspberrypi.org/documentation/linux/usage/users.md


Kotori
======
See :ref:`setup-debian`.

