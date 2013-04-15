Thermal monitor
===============

Tool for sending temperature readings to [Zabbix](http://www.zabbix.com)
monitoring software from 1-wire temperature sensors connected to
[Arduino](http://www.arduino.cc) on USB serial port.

Consists of command line tool written in [Python](http://www.python.org) and Arduino code.

Requirements
------------

### hardware

 * Arduino Duemilanove w/ ATmega328 or compatible platform
 * [DS18B20](http://www.maximintegrated.com/datasheet/index.mvp/id/2812) temperature sensor (connected on PIN 7)
 * USB cable
 * PC

### software

 * [OneWire library](http://www.pjrc.com/teensy/td_libs_OneWire.html) for Arduino
 * Python 2 (tested with 2.7)
 * [PySerial module](http://pyserial.sourceforge.net/)

License
-------

Copyright 2013 Michal Belica < *devel* at *beli* *sk* >

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/ .
```

You find a copy of the GNU General Public License in file LICENSE distributed
with the software.

