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

from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogLevelFilter
from wishbone.module import STDOUT
from wb_input_dictgenerator import DictGenerator
from wb_output_tcp import TCP
from wb_output_mongodb import MongoDB

from gevent import sleep, spawn

#Initialize router
router = Default(interval=1, context_switch=100, rescue=False, uuid=False)

#organize log flow
router.registerLogModule(LogLevelFilter, "loglevelfilter")
router.register(STDOUT, "stdout_logs")
router.connect("loglevelfilter.outbox", "stdout_logs.inbox")

#organize metric flow
router.registerMetricModule(Graphite, "graphite")
router.register(TCP, 'graphite_out', host="graphite-001", port=2013, stream=True )
router.connect("graphite.outbox", "graphite_out.inbox")

#organize event flow
router.register(DictGenerator, "dictgenerator", max_elements=10, sleep=1)
router.register(MongoDB, "mongodb", host="sandbox", capped=True, drop_db=False)
router.connect("dictgenerator.outbox", "mongodb.inbox")

#start
router.start()
router.block()