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

class Actor(gevent.Greenlet):

    def __init__(self, entrypoint):
        gevent.Greenlet.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % entrypoint)
        gl=gevent.spawn(self.__consume)
        self.counter=0
        gevent.spawn(self.measure)

    def __consume(self):
        while True:
            try:
                for event in self.socket.recv_multipart(flags=1):
                    self.consume(event)
            except:
                gevent.sleep(0.1)

    def consume(self, event):
        self.counter+=1

    def measure(self):
        previous=0
        while True:
            now=self.counter
            print now-previous
            previous=now
            gevent.sleep(1)



def main():
    actor=Actor("5667")
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:%s" % 5667)
    x=0
    while True:
        socket.send(str(x))
        x+=1

if __name__ == '__main__':
    main()