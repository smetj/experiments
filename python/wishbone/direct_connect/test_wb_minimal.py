#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_input_amqp.py
#
# Run with wishbone version >= 0.4.4

from wishbone import Actor
from wishbone.router import Default
from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import STDOUT
from wb_output_tcp import TCP

from gevent import sleep, spawn

class XGenerator(Actor):
    def __init__(self, name):
        Actor.__init__(self, name, setupbasic=False)
        self.createQueue("outbox")
        spawn(self.generate)

    def generate(self):
        context_switch_loop = self.getContextSwitcher(100, self.loop)
        while context_switch_loop.do():
            try:
                self.queuepool.outbox.put({"header":{},"data":"X"})
            except:
                break

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)

#Organize log flow
router.registerLogModule(STDOUT, "stdout")

#Organize metric flow
router.registerMetricModule(Graphite, "graphite")
router.register(TCP, 'graphite_out', host="graphite-001", port=2013)
router.connect("graphite.outbox", "graphite_out.inbox")

#Organize data flow
router.register(XGenerator, "xgenerator")
router.register(Null, "null")
router.connect("xgenerator.outbox", "null.inbox")

#start
router.start()
router.block()