#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#
# Run with wishbone version >= 0.4

from wishbone import Actor
from wishbone.router import Default

from wishbone.module import Null
from wishbone.module import LogLevelFilter
from wishbone.module import STDOUT
from wishbone.module import Graphite
from wb_output_tcp import TCP
from wb_input_amqp import AMQP
from wishbone.errors import QueueFull, QueueLocked


from gevent import sleep, spawn

class Forwarder(Actor):
    def __init__(self, name):
        Actor.__init__(self, name, setupbasic=True)

    def consume(self, event):
        try:
            #self.logging.info("Received event.")
            self.queuepool.outbox.put(event)
        except QueueLocked:
            self.queuepool.inbox.rescue(event)
            self.queuepool.inbox.putLock()
            self.queuepool.outbox.waitUntilPutAllowed()
            self.queuepool.inbox.putUnlock()

class Output(Actor):
    def __init__(self, name, size=1000):
        Actor.__init__(self, name, setupbasic=False)
        self.createQueue("inbox", size)
        self.registerConsumer(self.consume, self.queuepool.inbox)

    def consume(self, event):
        pass
        #self.logging.info("Received event.")
        #sleep(0.005)

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)

#Organize log flow
router.registerLogModule(LogLevelFilter, "loglevelfilter", max_level=7)
router.register(STDOUT, "stdout")
router.connect("loglevelfilter.outbox", "stdout.inbox")

#Organize metric flow
router.registerMetricModule(Null, "null")
# router.registerMetricModule(Graphite, "graphite")
# router.register(TCP, "graphite_transport", host="graphite-001", port=2013)
# router.connect("graphite.outbox", "graphite_transport.inbox")

#Organize data flow
router.register(AMQP, "amqp", host="localhost", queue="test", prefetch_count=100, no_ack=True)
router.register(Forwarder, "forwarder")
router.register(Output, "output")

router.connect("amqp.outbox", "forwarder.inbox")
router.connect("forwarder.outbox", "output.inbox")

#start
router.start()
router.block()
