#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  wb.py
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
from wishbone.logging import STDOUT as logs_STDOUT
from wishbone.metrics import Graphite
from wishbone.tools import Measure
from gevent import sleep, spawn
from wb_tcpclient import TCPClient
from wb_tippingbucket import TippingBucket


class NumberGenerator(Actor):
    def __init__(self, name):
        Actor.__init__(self, name, limit=0)
        spawn(self.run)

    def consume(self, event):
        pass

    def run(self):
        x=0
        # for x in xrange(10):
        #     self.queuepool.outbox.put({"header":{},"data":x})
        while self.loop():
            try:
                self.queuepool.outbox.put({"header":{},"data":x})
                x+=1
                sleep()
            except:
                break

class Null(Actor):
    def __init__(self, name):
        Actor.__init__(self, name, limit=0)

    @Measure.runTime
    def consume(self, event):
        pass
        #self.logging.info("Processing event: %s"%(event["data"]))
        #sleep(2)

numbergenerator=NumberGenerator("Numbergenerator")
null=Null("Null")
logging=logs_STDOUT("Logging", debug=False)
graphite=Graphite("Graphite")
tcpout=TCPClient("TCPout", pool=["graphite-001:2013"])
buffer=TippingBucket("buffer", age=10, events=100)

router = Default(interval=1, rescue=False)

router.register(logging)
router.register(graphite)
router.register(numbergenerator)
router.register(null)
router.register(tcpout)
router.register(buffer)

router.connect(router.logs, logging.queuepool.inbox)
router.connect(router.metrics, graphite.queuepool.inbox)
router.connect(graphite.queuepool.outbox, buffer.queuepool.inbox)
router.connect(buffer.queuepool.outbox,tcpout.queuepool.inbox)
router.connect(numbergenerator.queuepool.outbox, null.queuepool.inbox)

router.start()
router.block()