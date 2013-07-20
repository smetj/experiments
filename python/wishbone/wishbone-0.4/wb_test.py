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
from wishbone.tools import Measure
from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogFormatFilter
from wishbone.module import STDOUT


from gevent import sleep, spawn
from wb_tcpclient import TCPClient
from wb_tippingbucket import TippingBucket
from wb_msgpack import Msgpack
from wb_udsclient import UDSClient
from wb_udsserver import UDSServer

from os import getpid

#Create router
router = Default(interval=1, rescue=False)

#Register the logging & metric modules
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=False)
router.registerMetricModule((Graphite, "graphite", 0), "inbox")

#Register all actors
router.register((STDOUT, "stdout", 0), purge=True)
router.register((TippingBucket, "buffer", 0), age=10, events=100)
router.register((TCPClient, "tcpout", 0), pool=["graphite-001:2013"])
router.register((UDSServer, "udsserver", 0), pool=4000)
router.register((Msgpack, "msgpack", 0), mode="unpack")
router.register((Null, "null", 0))

#Logs
router.connect("logformatfilter.outbox", "stdout.inbox")

#Metrics
router.connect("graphite.outbox", "buffer.inbox")
router.connect("buffer.outbox", "tcpout.inbox")

#events
router.connect("udsserver.inbox", "msgpack.inbox")
router.connect("msgpack.outbox", "null.inbox")

#Start
router.start()
router.block()