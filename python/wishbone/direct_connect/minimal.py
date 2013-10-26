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

from wishbone import Actor
from wishbone.router import Default
from wishbone.module import STDOUT
from gevent import spawn, sleep
import gevent_profiler

class Input(Actor):
    def __init__(self, name):
        Actor.__init__(self, name)
        spawn(self.generate)

    def generate(self):
        while self.loop():
            event = {"header":{},"data":"X"}
            self.logging.info("Generated event.")
            #print self.queuepool.outbox
            self.queuepool.outbox.put(event)
            sleep(0.5)


class Output(Actor):
    def __init__(self, name, size=1):
        Actor.__init__(self, name)
        self.createQueue("inbox")
        self.registerConsumer(self.consume, self.queuepool.inbox)

    def consume(self, event):
        self.logging.info("Received event.")
        sleep(0.5)


# gevent_profiler.set_stats_output('my-stats.txt')
# gevent_profiler.set_summary_output('my-summary.txt')
# gevent_profiler.set_trace_output('my-trace.txt')

# gevent_profiler.attach()

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)
router.registerLogModule(STDOUT, "logs_out")
router.registerMetricModule(STDOUT, "metrics_out")

router.register(Input, "input")
router.register(Output, "output")

router.connect("input.outbox", "output.inbox")

#start
router.start()
router.block()

# gevent_profiler.detach()
