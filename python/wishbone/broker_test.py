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
from wishbone.module import Fanout
from wishbone.module import Header
from wishbone.module import TippingBucket

from wb_amqp import AMQP
from wb_gearmand import Gearmand
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
                self.queuepool.outbox.put({"header":{'broker_exchange':"", 'broker_key':"test", 'broker_tag':"test"},"data":str(x)})
                x+=1
                looper+=1
            except:
                break


#Initialize router
router = Default(interval=1, rescue=False, uuid=False)
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=False)
router.registerMetricModule((Graphite, "graphite", 0), "inbox")
router.register((STDOUT, "stdout", 0))
router.register((Null, "null", 0))
router.connect("logformatfilter.outbox", "stdout.inbox")
router.connect("graphite.outbox", "null.inbox")

#Feedback loop
router.register((Header, "header", 0), header={'broker_exchange':"", 'broker_key':"test", 'broker_tag':"test"})
router.register((AMQP, "broker", 0), host="sandbox", consume_queue="test")
router.connect("broker.inbox", "header.inbox")
router.connect("header.outbox", "broker.outbox")

#Produce events
# router.register((NumberGenerator, "numbergenerator", 0))
# router.register((Header, "header", 0), header={'broker_exchange':"", 'broker_key':"test", 'broker_tag':"test"})
# router.register((AMQP, "broker", 0), host="sandbox")
# router.connect("numbergenerator.outbox", "header.inbox")
# router.connect("header.outbox", "broker.outbox")

#Consume events to STDOUT
# router.register((AMQP, "broker", 0), host="sandbox", consume_queue="test")
# router.register((STDOUT, "events_stdout", 0))
# router.connect("broker.inbox", "events_stdout.inbox")

#start
router.start()
router.block()