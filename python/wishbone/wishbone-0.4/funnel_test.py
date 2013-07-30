#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  fanout_test.py
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

from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogFormatFilter
from wishbone.module import STDOUT
from wishbone.module import Funnel

from wb_tcpclient import TCPClient
from wb_tippingbucket import TippingBucket
from wb_msgpack import Msgpack
from wb_udsclient import UDSClient
from wb_udsserver import UDSServer
from gevent import sleep, spawn

class NumberGenerator(Actor):
    def __init__(self, name, limit=0):
        Actor.__init__(self, name, limit=limit)
        spawn(self.run)

    def consume(self, event):
        pass

    def run(self):
        x=0
        looper=0
        while self.loop():
            try:
                if looper == 100:
                    looper=0
                    sleep()
                self.queuepool.outbox.put({"header":{},"data":str(x)})
                x+=1
                looper+=1
            except:
                break


router = Default(interval=1, rescue=False, uuid=False)
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=False)
router.registerMetricModule((Graphite, "graphite", 0), "inbox")

router.register((STDOUT, "stdout_logs", 0))
router.register((STDOUT, "stdout", 0))
router.register((NumberGenerator, "numbergenerator1", 0))
router.register((NumberGenerator, "numbergenerator2", 0))
router.register((Funnel, "funnel", 0))

#logs & metrics
router.connect("logformatfilter.outbox", "stdout_logs.inbox")

#events
router.connect("numbergenerator1.outbox", "funnel.one")
router.connect("numbergenerator2.outbox", "funnel.two")
router.connect("funnel.outbox", "stdout.inbox")

#start
router.start()
router.block()