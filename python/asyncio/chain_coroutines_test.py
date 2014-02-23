#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wishbone_test.py
#
#  Copyright 2014 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
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

import asyncio
import time
import random

class Input():
    def __init__(self):
        self.outbox = None

    @asyncio.coroutine
    def start(self):
        while True:
            (result, message) = yield from self.outbox("Start")
            yield from asyncio.sleep(0)
            if not result:
                print (message)

class AddLetter():

    def __init__(self, letter):
        self.inbox = self.consume
        self.outbox = None
        self.letter = letter

    @asyncio.coroutine
    def consume(self, event):
        try:
            if random.randint(0,10000) == 50:
                raise Exception("An exception occurred in step which adds letter %s"%(self.letter))
            data = "%s %s"%(event, self.letter)
        except Exception as err:
            return (False, err)
        else:
            (status, data) = yield from self.outbox(data)
            return (status, data)

class Output():

    def __init__(self):
        self.inbox = self.consume
        self.total = 0
        self.speed()

    @asyncio.coroutine
    def consume(self, data):
        self.total+=1
        try:
            # print (data)
            return (True,None)
        except Exception as err:
            return (False, err)

    @asyncio.coroutine
    def speed(self):
        previous_total = 0
        while True:
            print ( "Msg per second: %s"%(self.total - previous_total) )
            previous_total = self.total
            yield from asyncio.sleep(1)


def main():

    input = Input()
    a = AddLetter("A")
    b = AddLetter("B")
    c = AddLetter("C")
    d = AddLetter("D")
    output = Output()

    input.outbox = a.inbox
    a.outbox = b.inbox
    b.outbox = c.inbox
    c.outbox = d.inbox
    d.outbox = output.inbox

    tasks = [ asyncio.Task(input.start()), asyncio.Task(output.speed()) ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == '__main__':
    main()


