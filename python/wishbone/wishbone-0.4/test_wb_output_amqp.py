#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_output_amqp.py
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

from wishbone.module import Null
from wishbone.module import LogLevelFilter
from wishbone.module import STDOUT
from wishbone.module import Header
from wishbone.module import TestEvent
from wishbone.module import Fanout

from wb_output_amqp import AMQP
from wb_input_dictgenerator import DictGenerator
from gevent import sleep, spawn

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)

#organize metricstream
router.registerMetricModule(Null, "null")
# router.registerMetricModule(Graphite, "graphite")
# router.registerMetricModule(TCP, "graphite_transport", host=sandbox, port=2013)
# router.connect("graphite.outbox", "graphite_transport.inbox")

#organize logstream
router.registerLogModule(LogLevelFilter, "loglevelfilter")
router.register(STDOUT, "stdout_logs")
router.connect("loglevelfilter.outbox", "stdout_logs.inbox")

#router.register(TestEvent, "testevent", interval=1)
router.register(DictGenerator, "testevent", max_elements=10)
router.register(Header, "header", header={"amqp":{'broker_exchange':"test", 'broker_key':"test", 'broker_tag':"test"}})
router.register(STDOUT, "stdout", complete=True)
router.register(AMQP, "amqp", host="localhost")

router.connect("testevent.outbox", "header.inbox")
router.connect("header.outbox", "amqp.inbox")

#start
router.start()
router.block()