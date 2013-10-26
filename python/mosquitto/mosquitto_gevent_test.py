#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  mosquitto_gevent_test.py
#
#  Copyright 2013 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import gevent
#from gevent import monkey;monkey.patch_all
import mosquitto


class DoTheDance():

    def __init__(self):
        self.client = mosquitto.Mosquitto("test-client")
        self.client.connect("sandbox")
        #self.loop = gevent.spawn(self.looper)
        self.produce = gevent.spawn(self.producer)

        while True:
            gevent.sleep(1)

    def producer(self):
        counter=0
        while True:
            counter+=1
            if counter > 1000:
                counter=0
                self.client.loop()
            self.client.publish("my/topic", "hello world", 1)


    def looper(self):
        while True:

            gevent.sleep(1)

if __name__ == '__main__':
    dtd = DoTheDance()