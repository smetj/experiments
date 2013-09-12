#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#
# Run with wishbone version >= 0.4

from wishbone import Actor
from wishbone.router import Default

from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogLevelFilter
from wishbone.module import STDOUT
from wishbone.errors import QueueFull, QueueLocked

from gevent import sleep, spawn

class Input(Actor):
    def __init__(self, name):
        Actor.__init__(self, name, setupbasic=False)
        self.createQueue("outbox")
        spawn(self.generate)

    def generate(self):
        while self.loop():
            event = {"header":{},"data":"X"}
            self.logging.info("Generated event.")
            try:
                self.queuepool.outbox.put(event)
                sleep(0.1

class Forwarder(Actor):
    def __init__(self, name):
        Actor.__init__(self, name, setupbasic=True)

    def consume(self, event):
        try:
            self.logging.info("Received event.")
            self.queuepool.outbox.put(event)
        except QueueLocked:
            self.queuepool.inbox.rescue(event)
            self.queuepool.inbox.putLock()
            self.queuepool.outbox.waitUntilPutAllowed()
            self.queuepool.inbox.putUnlock()

class Output(Actor):
    def __init__(self, name, size=1):
        Actor.__init__(self, name, setupbasic=False)
        self.createQueue("inbox", size)
        self.registerConsumer(self.consume, self.queuepool.inbox)

    def consume(self, event):
        self.logging.info("Received event.")
        sleep(5)

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)

#Organize log flow
router.registerLogModule(LogLevelFilter, "loglevelfilter")
router.register(STDOUT, "stdout")
router.connect("loglevelfilter.outbox", "stdout.inbox")

#Organize metric flow
router.registerMetricModule(Null, "null")

#Organize data flow
router.register(Input, "input")
router.register(Forwarder, "forwarder")
router.register(Output, "output")

router.connect("input.outbox", "forwarder.inbox")
router.connect("forwarder.outbox", "output.inbox")

#start
router.start()
router.block()
