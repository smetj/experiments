#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_wait_seconds.py
#
# Run with wishbone version >= 0.4

from wishbone import Actor
from wishbone.router import Default
from wishbone.tools import Measure, LoopContextSwitcher

from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogFormatFilter
from wishbone.module import STDOUT

from wb_output_tcp import TCP
from wb_output_waitseconds import WaitSeconds

from gevent import sleep, spawn
from wishbone.errors import QueueFull

class XGenerator(Actor, LoopContextSwitcher):
    def __init__(self, name, max_size=10):
        Actor.__init__(self, name, setupbasic=False)
        self.createQueue("outbox", max_size)
        spawn(self.generate)

    def generate(self):
        context_switch_loop = self.getContextSwitcher(75, self.loop)

        while context_switch_loop.do():
            try:
                self.queuepool.outbox.put({"header":{},"data":"X"})
            except QueueFull:
                sleeping = (self.queuepool.outbox.stats()["out_rate"])+0.1
                self.logging.info("Oops queue full waiting for %s seconds."%(sleeping))
                sleep(sleeping)

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)

#Organize log flow
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=False)
router.register((STDOUT, "stdout", 0))
router.connect("logformatfilter.outbox", "stdout.inbox")

#Organize metric flow
router.registerMetricModule((Graphite, "graphite", 0), "inbox")
router.register((TCP, 'graphite_out', 0), host="graphite-001", port=2013, stream=True )
router.connect("graphite.outbox", "graphite_out.inbox")

#Organize data flow
router.register((XGenerator, "xgenerator", 0))
router.register((WaitSeconds, "waitseconds", 0), seconds=0.5, max_size=10)
router.connect("xgenerator.outbox", "waitseconds.inbox")

#start
router.start()
router.block()