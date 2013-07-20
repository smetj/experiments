#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_input_amqp.py
#
# Run with wishbone version >= 0.4

from wishbone import Actor
from wishbone.router import Default
from wishbone.tools import Measure

from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogFormatFilter
from wishbone.module import STDOUT
from wb_output_tcp import TCP

from gevent import sleep, spawn

class XGenerator(Actor):
    def __init__(self, name):
        Actor.__init__(self, name, setupbasic=False)
        self.createQueue("outbox")
        spawn(self.generate)

    def generate(self):
        looper=0
        while self.loop():
            try:
                if looper == 75:
                    looper=0
                    sleep()
                self.queuepool.outbox.put({"header":{},"data":"X"})
                looper+=1
            except:
                break

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)

#Organize log flow
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=False)
router.register((STDOUT, "stdout", 0), purge=True)
router.connect("logformatfilter.outbox", "stdout.inbox")

#Organize metric flow
router.registerMetricModule((Graphite, "graphite", 0), "inbox")
router.register((TCP, 'graphite_out', 0), host="graphite-001", port=2013, stream=True )
router.connect("graphite.outbox", "graphite_out.inbox")

#Organize data flow
router.register((XGenerator, "xgenerator", 0))
router.register((Null, "null", 0))
router.connect("xgenerator.outbox", "null.inbox")

#start
router.start()
router.block()