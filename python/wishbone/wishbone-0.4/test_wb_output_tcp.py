#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_input_amqp.py
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

from wishbone import Actor
from wishbone.router import Default
from wishbone.tools import Measure
from wishbone.tools import LoopContextSwitcher
from wishbone.errors import QueueLocked, QueueFull

from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogFormatFilter
from wishbone.module import STDOUT
from wb_output_tcp import TCP

from gevent import sleep, spawn

#nc -kl 10000|pv -r --line-mode > /dev/null

class XGenerator(Actor, LoopContextSwitcher):

    def __init__(self, name):
        Actor.__init__(self, name, setupbasic=False)
        self.createQueue("outbox", max_size=0)
        spawn(self.generate)

    def generate(self):
        context_switch_loop = self.getContextSwitcher(75, self.loop)
        while context_switch_loop.do():
            try:
                self.queuepool.outbox.put({"header":{},"data":"X\n"})
            except QueueLocked, QueueFull:
                sleep(1)

#Initialize router
router = Default(interval=1, context_switch=50, rescue=False, uuid=False)

#Organize log flow
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=True)
router.register((STDOUT, "stdout", 0))
router.connect("logformatfilter.outbox", "stdout.inbox")

#Organize metric flow
router.registerMetricModule((Graphite, "graphite", 0), "inbox")
router.register((TCP, 'graphite_out', 0), host="graphite-001", port=2013, stream=True )
router.connect("graphite.outbox", "graphite_out.inbox")

#Organize data flow
router.register((XGenerator, "xgenerator", 0))
router.register((TCP, "tcp", 0), host="localhost", port=10000, stream=True, rescue=True )
router.connect("xgenerator.outbox", "tcp.inbox")

#start
router.start()
router.block()