#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wb.py
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
import gevent
from gevent import sleep, spawn
from gevent import queue
from gevent import pool
from gevent import signal
from uuid import uuid4

class Stage():

    def __init__(self, name, **kwargs):
        self.name=name
        self.inbox = queue.Queue(maxsize=1)
        self.outbox = queue.Queue(maxsize=1)
        self.admin = queue.Queue(maxsize=1)
        self.exit=False

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        pass

    def start(self):
        while not self.exit:
            try:
                event = self.inbox.get(timeout=0.01)
                self.consume(event)
            except gevent.queue.Empty:
                pass

    def stop(self):
        self.exit = True
        self.log("Stop received")

    def consume(self, event):
        self.outbox.put(event)

    def _startAdmin(self):
        while not self.exit:
            try:
                event = self.admin.get(timeout=0.01)
            except gevent.queue.Empty:
                pass
            else:
                self.log("Received admin event %s"%(event["data"]))
                if event["header"]["target"] == self.name or event["header"]["target"] == "*":
                    spawn(getattr(self, event["data"]))

    def log(self, message):
        print "%s - %s"%(self.name, message)

class Pulse(Stage):
    def __init__(self, name, interval):
        Stage.__init__(self, name)
        self.interval=interval

    def start(self):
        while not self.exit:
            self.outbox.put({"header":{},"data":{}}, block=True)
            sleep(self.interval)

class STDOUT(Stage):
    def __init__(self, name):
        Stage.__init__(self, name)
        self.counter = 0
        spawn(self.speed)

    def consume(self, event):
        #print event
        self.counter += 1

    def speed(self):
        temp = 0
        while not self.exit:
            now = self.counter
            print "Speed at %s msg/s"%(now-temp)
            temp=now
            sleep(1)

class DefaultV2:

    def __init__(self, name=None):
        self.name=name
        self.modules={}
        self.refcount = 0
        self.pool=pool.Group()
        if self.name == None:
            self.name = str(uuid4())

    def block(self):
        self.pool.join()

    def connect(self, source, destination):
        self._waitForRefcount()
        (smodule, squeue) = source.split(".")
        (dmodule, dqueue) = destination.split(".")
        s = getattr(self.modules[smodule], squeue)
        setattr(self.modules[dmodule], dqueue, s)

    def start(self):
        self._waitForRefcount()
        for module in self.modules:
            self.modules[module].admin.put({"header":{"target":"*"},"data":"start"})

    def stop(self):
        for module in self.modules:
            self.modules[module].admin.put({"header":{"target":"*"},"data":"stop"})

    def register(self, module, name, **kwargs):
        self.refcount += 1
        self.pool.spawn(self._spawnStart, module, name, **kwargs)

    def _spawnStart(self, module, name, **kwargs):
        with module(name, **kwargs) as stage:
            self.modules[name] = stage
            stage._startAdmin()

    def _waitForRefcount(self):
        while self.refcount != len(self.modules):
            sleep(0.001)

    def __enter__(self):
        signal(2, self.__signal_handler)
        return self

    def __exit__(self, exception, value, traceback):
        self.pool.join()

    def __signal_handler(self):
        self.stop()

def main():

    with DefaultV2() as router:
        router.register(Pulse, "pulse", interval=0)
        router.register(Stage, "forward1")
        router.register(Stage, "forward2")
        router.register(Stage, "forward3")
        router.register(Stage, "forward4")
        router.register(Stage, "forward5")
        router.register(Stage, "forward6")
        router.register(Stage, "forward7")
        router.register(Stage, "forward8")
        router.register(Stage, "forward9")
        router.register(Stage, "forward10")
        router.register(Stage, "forward11")
        router.register(Stage, "forward12")
        router.register(Stage, "forward13")
        router.register(Stage, "forward14")
        router.register(Stage, "forward15")
        router.register(Stage, "forward16")
        router.register(Stage, "forward17")
        router.register(Stage, "forward18")
        router.register(Stage, "forward19")
        router.register(Stage, "forward20")
        router.register(STDOUT, "stdout")
        router.connect("pulse.outbox", "forward1.inbox")
        router.connect("forward1.outbox", "forward2.inbox")
        router.connect("forward2.outbox", "forward3.inbox")
        router.connect("forward3.outbox", "forward4.inbox")
        router.connect("forward4.outbox", "forward5.inbox")
        router.connect("forward5.outbox", "forward6.inbox")
        router.connect("forward6.outbox", "forward7.inbox")
        router.connect("forward7.outbox", "forward8.inbox")
        router.connect("forward8.outbox", "forward9.inbox")
        router.connect("forward9.outbox", "forward10.inbox")
        router.connect("forward10.outbox", "forward11.inbox")
        router.connect("forward11.outbox", "forward12.inbox")
        router.connect("forward12.outbox", "forward13.inbox")
        router.connect("forward13.outbox", "forward14.inbox")
        router.connect("forward14.outbox", "forward15.inbox")
        router.connect("forward15.outbox", "forward16.inbox")
        router.connect("forward16.outbox", "forward17.inbox")
        router.connect("forward17.outbox", "forward18.inbox")
        router.connect("forward18.outbox", "forward19.inbox")
        router.connect("forward19.outbox", "forward20.inbox")
        router.connect("forward20.outbox", "stdout.inbox")
        router.start()
        router.block()

if __name__ == "__main__":
    main()