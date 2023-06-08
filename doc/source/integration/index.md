(integrations)=
(kotori-decoders)=
# Integrations

Integration adapter and decoder components will know about device- or platform-
specific payload formats, and will decode telemetry messages appropriately and
mostly transparently.

This documentation section enumerates the collection of integrations shipped
with Kotori. Adding more integrations is possible.


```{toctree}
:caption: Protocols
:maxdepth: 1
:hidden:

../handbook/acquisition/protocol/mqtt
../handbook/acquisition/protocol/http
```

```{toctree}
:caption: Device/vendor integrations
:maxdepth: 1
:hidden:

airrohr
tasmota
tts-ttn
```


## Protocols

::::::{grid} 1
:margin: 0
:padding: 0

:::::{grid-item-card}
::::{grid} 2
:margin: 0
:padding: 0

:::{grid-item}
:columns: 8
#### [](#daq-mqtt)

Measurement readings can be acquired through MQTT, using JSON, or other payload formats.

<small>
<strong>Categories:</strong> generic, baseline, networking
</small>
:::
:::{grid-item}
:columns: 4
{bdg-primary-line}`eth` {bdg-primary-line}`wifi` {bdg-primary-line}`mqtt`

{bdg-success-line}`ANY` 

{bdg-secondary-line}`ANY`
:::
::::
:::::

::::::


::::::{grid} 1
:margin: 0
:padding: 0

:::::{grid-item-card}
::::{grid} 2
:margin: 0
:padding: 0

:::{grid-item}
:columns: 8
#### [](#daq-http)

Measurement readings can be acquired through HTTP, using JSON, CSV, or other payload formats.

<small>
<strong>Categories:</strong> generic, baseline, networking
</small>
:::
:::{grid-item}
:columns: 4
{bdg-primary-line}`eth` {bdg-primary-line}`wifi` {bdg-primary-line}`http`

{bdg-success-line}`ANY` 

{bdg-secondary-line}`ANY`
:::
::::
:::::

::::::



## Device/vendor integrations

::::::{grid} 1
:margin: 0
:padding: 0

:::::{grid-item-card}
::::{grid} 2
:margin: 0
:padding: 0

:::{grid-item}
:columns: 8
#### [](#integration-airrohr)

Receive and record telemetry data from air particulate measurement devices of the
Sensor.Community (formerly Luftdaten.Info) project, running the Airrohr Firmware.

<small>
<strong>Categories:</strong> environmental monitoring, citizen science, multi-sensor,
global sensor network
</small>
:::
:::{grid-item}
:columns: 4
{bdg-primary-line}`wifi` {bdg-primary-line}`http` {bdg-primary-line}`influxdb` {bdg-primary-line}`csv` {bdg-primary-line}`json`

{bdg-success-line}`SPS30` {bdg-success-line}`SDS011` {bdg-success-line}`BMP180` {bdg-success-line}`BMP/E 280` {bdg-success-line}`NEO-6M` {bdg-success-line}`DHT22` 

{bdg-secondary-line}`esp8266`
:::
::::
:::::

::::::


::::::{grid} 1
:margin: 0
:padding: 0

:::::{grid-item-card}
::::{grid} 2
:margin: 0
:padding: 0

:::{grid-item}
:columns: 8
#### [](#integration-tasmota)

Receive and record telemetry data over MQTT, from devices running the Tasmota firmware.

<small>
<strong>Categories:</strong> polyglot, multi-sensor, multi-device, open source framework, MQTT
</small>
:::
:::{grid-item}
:columns: 4
{bdg-primary-line}`wifi` {bdg-primary-line}`mqtt` {bdg-primary-line}`json`

{bdg-success-line}`MANY`

{bdg-secondary-line}`esp8266` {bdg-secondary-line}`esp32`
:::
::::
:::::

::::::


::::::{grid} 1
:margin: 0
:padding: 0

:::::{grid-item-card}
::::{grid} 2
:margin: 0
:padding: 0

:::{grid-item}
:columns: 8
#### [](#integration-tts-ttn)

Receive and decode telemetry data from devices on the LoRaWAN network controller
implementation The Things Stack (TTS) / The Things Network (TTN), using HTTP
webhooks, and store it into timeseries databases for near real-time querying.

<small>
<strong>Categories:</strong> polyglot, multi-sensor, multi-device, LoRaWAN
</small>
:::
:::{grid-item}
:columns: 4
{bdg-primary-line}`rf/ism` {bdg-primary-line}`lorawan` {bdg-primary-line}`json`

{bdg-success-line}`MANY`

{bdg-secondary-line}`MANY`
:::
::::
:::::

::::::
