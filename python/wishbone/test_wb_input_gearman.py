#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_input_gearman.py
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
from wb_input_tcp import TCP
from wb_input_gearman import Gearman

#Initialize router
router = Default(interval=1, rescue=False, uuid=False)
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=True)
router.registerMetricModule((Graphite, "graphite", 0), "inbox")
router.register((STDOUT, "stdout", 0))
router.register((Null, "null", 0))
router.connect("logformatfilter.outbox", "stdout.inbox")
router.connect("graphite.outbox", "null.inbox")

#Consume events to STDOUT
router.register((Gearman, "gearman", 0), hostlist=["besrvuc-nag02:4730"], queue="perfdata", workers=10, secret="Aloh9uibshojeF8oAhyo3eefGu5ohr3iDeek4ehamaM9eisoas6OoveiareQuo0i")
router.register((STDOUT, "stdout_events", 0))


router.connect("gearman.outbox", "stdout_events.inbox")

#start
router.start()
router.block()