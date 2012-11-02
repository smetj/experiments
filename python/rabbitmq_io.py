#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rabbitmq_io.py
#  
#  Copyright 2012 Jelle Smet development@smetj.net
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
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

from wishbone import Wishbone
from wishbone.server import ParallelServer
from logging import DEBUG, INFO

def setup():
        wb = Wishbone()
        wb.registerModule ( ('wishbone.io_modules.broker', 'Broker', 'broker'), host='sandbox', vhost='/', username='guest', password='guest', consume_queue='rabbitmq_io', prefetch_count=100, no_ack=False )
        wb.registerModule ( ('wishbone.modules.brokerloopback', 'BrokerLoopback', 'brokerloopback'), key='rabbitmq_io', exchange='', dump=10000 )
        wb.connect (wb.broker.inbox, wb.brokerloopback.inbox)
        wb.connect (wb.brokerloopback.outbox, wb.broker.outbox)
        wb.start()
        
def main():        
    server = ParallelServer(instances=1, setup=setup, daemonize=False, name='rabbitmq_io', log_level=INFO)
    server.start()

if __name__ == '__main__':
    
    main()
