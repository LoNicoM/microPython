microPython garage door opener for ESP8266.

this microcontroller project, I feel is robust enough for human consumption.

you will need to install umqtt.simple with:

upip.install("micropython-umqtt.simple")

from the webREPL

you will need to upload the files to your esp8266.

also you will need an MQTT broker, i recommend mosquitto.
can be installed on a raspberry pi, or another low power SBC
or even on your router if its capable of installing optware.
