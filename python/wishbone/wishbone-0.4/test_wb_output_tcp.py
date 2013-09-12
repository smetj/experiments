#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_output_tcp.py
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

from wb_output_tcp import TCP
from gevent import sleep, spawn

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)

#organize eventstream
router.registerMetricModule(Null, "null")

#organize logstream
router.registerLogModule(LogLevelFilter, "loglevelfilter")
router.register(STDOUT, "stdout_logs")
router.connect("loglevelfilter.outbox", "stdout_logs.inbox")

router.register(TestEvent, "testevent")
router.register(TCP, "tcp", host="localhost")

router.connect("testevent.outbox", "tcp.inbox")

#start
router.start()
router.block()