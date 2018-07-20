# MIT License
# 
# Copyright (c) 2018 deathwish.xyz
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This file is executed on every boot (including wake-boot from deepsleep)

import ujson as json
from ntptime import settime
import network
import webrepl
import gc

config = json.loads(open('config.json').read())

def wifi_ap_disable():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    print('network ap status:', ap_if.active())

def wifi_do_connect(essid, password, hostname):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to', essid, 'network...')
        sta_if.active(True)
        sta_if.config(dhcp_hostname=hostname)
        sta_if.connect(essid, password)
        while not sta_if.isconnected():
            pass
    print('network config:')
    print(sta_if.ifconfig())

def time_ntp():
    print('local time is:')
    settime()


wifi_ap_disable()
wifi_do_connect(
    essid = config['wifi']['ssid'],
    password = config['wifi']['password'],
    hostname = config['project']['name'])
time_ntp()
webrepl.start()
gc.collect()
