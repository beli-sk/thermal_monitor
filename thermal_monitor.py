#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# Thermal monitor
#
# Copyright 2013 Michal Belica <devel@beli.sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import serial
import sys
import signal
import select
import re
import time
import subprocess
from optparse import OptionParser

def zabbix_sender(options, data):
    proc = subprocess.Popen(['zabbix_sender', '-z', options.zabbix, '-p', options.port
            , '-s', options.host, '-i', '-'], stdin=subprocess.PIPE)
    for addr,temp in data.items():
        proc.communicate('- %s[%s] %g\n' % (options.key, addr, temp))
    proc.stdin.close()
    proc.wait()

parser = OptionParser()
parser.add_option("-d", "--device", dest="device",
        help="read from serial port DEVICE (required)", metavar="DEVICE")
parser.add_option("-s", "--speed", dest="speed", type="int", default=9600,
        help="serial port baud rate (default: 9600)", metavar="BAUD")
parser.add_option("-i", "--interval", dest="interval", type="int", default=10,
        help="sampling interval (default: 10)", metavar="SECONDS")
parser.add_option("-z", "--zabbix", dest="zabbix",
        help="Zabbix server (required)", metavar="ADDR")
parser.add_option("-p", "--port", dest="port", default="10051",
        help="listening port of Zabbix server (default: 10051)", metavar="PORT")
parser.add_option("-n", "--host", dest="host",
        help="name of host in Zabbix (required)", metavar="NAME")
parser.add_option("-k", "--key", dest="key", default="thermal_monitor",
        help="item key base name; device address will be added as an argument, "
        +"e.g. thermal_monitor[addr] (default: thermal_monitor)", metavar="key")
(options, args) = parser.parse_args()

# check for required options
for opt in ['device', 'zabbix', 'host']:
    if opt not in options.__dict__ or options.__dict__[opt] is None:
        parser.error("parameter --%s is required" % opt)

running = True

def sighandler_exit(signum, frame):
    global running
    running = False

signal.signal(signal.SIGINT, sighandler_exit)
signal.signal(signal.SIGTERM, sighandler_exit)
signal.signal(signal.SIGHUP, sighandler_exit)

ser = serial.Serial(options.device, options.speed)
ser.readline() # ignore first (incomplete) line

cre = re.compile(r"R=(?P<addr>\w+)\s+T=(?P<temp>[.0-9]+)\r?$")

next = time.time()

data = dict()
sent = False

while running:
    try:
        line = ser.readline()
    except select.error as e:
        if e[0] == 4: # interrupted system call
            continue
        else:
            raise
    if time.time() > next:
        next += options.interval
        # clears the list to send all addresses again
        for k,v in data.items():
            data[k] = None
        sent = False
    elif sent:
        # data already sent in this cycle
        continue
    m = cre.search(line)
    if m:
        # line matched pattern
        addr = m.group('addr')
        temp = float(m.group('temp'))
        if addr not in data or data[addr] is None:
            # address not yet collected in this cycle
            data[addr] = temp
        else:
            # repeating address reached - send out data
            print "sending", addr, temp
            zabbix_sender(options, data)
            sent = True
    else:
        print "invalid line received"

ser.close()
