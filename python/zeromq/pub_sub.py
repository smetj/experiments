#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#
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

import zmq.green as zmq
import gevent
from random import randint
import sys
from time import time

class Router():
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("inproc://blah")
        gevent.spawn(self.produce)

    def produce(self):
        while True:
            self.socket.send("%s test"%(["one,","two","three"][randint(0,2)]))
            gevent.sleep()


class Consumer():
    def __init__(self, topic):
        self.counter=0
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("inproc://blah")
        self.topic=topic
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)
        gevent.spawn(self.consume)
        #help(self.socket)
    def consume(self):
        while True:
            for message in self.socket.recv_multipart():
                self.counter+=1

def main():
    router=Router()
    consumer_one=Consumer("one")
    consumer_two=Consumer("two")
    consumer_two=Consumer("three")
    previous_value=0

    while True:
        now = consumer_one.counter
        print now - previous_value
        previous_value = now

        gevent.sleep(1)

if __name__ == '__main__':
    main()