#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  compare_direct_q_vs_routing_logic.py
#
#  Copyright 2012 Jelle Smet <development@smetj.net>
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

from testlap import TestLap
import gevent

from gevent import queue
from gevent import monkey;monkey.patch_all()

class dummyQueue():
    '''Creates an input and output queue and shovels data between them.'''

    def __init__(self,instance,end=False):
        self.input_queue=queue.Queue()
        self.output_queue=queue.Queue()
        self.instance=instance
        self.end=end

    def shovel(self):
        while True:
            gevent.sleep(0)
            try:
                message = self.input_queue.get(block=False)
            except:
                pass
            else:
                if self.end == False:
                    #print ("%s processed message."%self.instance)
                    self.output_queue.put(message)
                else:
                    #print ("%s Elvis has left the building."%self.instance)
                    pass
                if message == 'kill':
                        break

class dummyQueue2():

    '''Creates an input and output queue and shovels data between them.
    Handles RouterIO wrapper data.'''

    def __init__(self,instance,end=False, router_queue=None):
        self.input_queue=queue.Queue()
        self.output_queue=router_queue
        self.instance=instance
        self.end=end

    def shovel(self):
        while True:
            gevent.sleep(0)
            try:
                message = self.input_queue.get(block=False)
            except:
                pass
            else:
                if self.end == False:
                    #print ("%s processed message."%self.instance)
                    self.output_queue.put({"source":self.instance,"data":message})
                else:
                    #print ("%s Elvis has left the building."%self.instance)
                    pass
                if message == 'kill':
                        break                        

class WishboneIO():

    '''A class which orchestrates the IO between modules using 1 queue per connection (Wishbone Style).'''

    def __init__(self,jumps=3, messages=50000):
        self.jumps=jumps-1
        self.messages=messages
        self.lock=True
        self.instances=[]
        self.backgrounds=[]
        for instance in range(self.jumps):
            self.instances.append(dummyQueue(instance))
            self.backgrounds.append(gevent.Greenlet.spawn(self.instances[instance].shovel))
        self.instances.append(dummyQueue(instance+1,True))
        self.backgrounds.append(gevent.Greenlet.spawn(self.instances[-1].shovel))
        for index,item in enumerate(self.instances):
            if index != len(self.instances)-1:
                self.backgrounds.append(gevent.Greenlet.spawn(self.connector, self.instances[index], self.instances[index+1]))

    def connector(self, input_instance, output_instance):

        '''The connector actually shoveling messages.'''

        input_queue = getattr(input_instance,'output_queue')
        output_queue = getattr(output_instance,'input_queue')
        while True:
            gevent.sleep(0)
            try:
                message = input_queue.get(block=False)
            except:
                pass
            else:
                output_queue.put(message)
                if message == 'kill':
                    break

    def go(self):

        for _ in range(self.messages):
            self.instances[0].input_queue.put('x')
        self.instances[0].input_queue.put('kill')
        gevent.joinall(self.backgrounds)

class RouterIO():
    
    '''A class which orchestrates the IO between modules using 1 queue with routing data.'''
    
    def __init__(self,routing_table={}, jumps=3, messages=10000):
        self.input_queue=queue.Queue()
        self.module_input_queues={}
        self.jumps=jumps-1
        self.messages=messages
        self.routing_table=routing_table
        self.instances=[]
        self.backgrounds=[]
        self.setup()
    
    def setup(self):
        for instance in range(self.jumps):
            self.instances.append(dummyQueue2(str(instance),router_queue=self.input_queue))
        self.instances.append(dummyQueue2(str(instance+1),end=True,router_queue=self.input_queue))
        for instance in self.instances:
            self.register(instance.instance,getattr(instance,'input_queue'))
            self.backgrounds.append(gevent.Greenlet.spawn(instance.shovel))
        self.routing_table=self.buildRouterTable(self.jumps)
        self.router=gevent.Greenlet.spawn(self.do)

    def register(self, name, module_queue):
        self.module_input_queues[name]=module_queue
    
    def buildRouterTable(self, number):
        table={}
        for step in range(number+1):
            table[str(step)]=[str(step+1)]
        return table
            
    
    def do(self):
        while True:
            gevent.sleep(0)
            try:
                message = self.input_queue.get(block=False)
            except:
                pass
            else:
                if message['source'] in self.routing_table:
                    for route in self.routing_table[message['source']]:
                        self.module_input_queues[route].put(message['data'])
                else:
                    print "Source %s is not in routing table"%message['source']
                                    
    def go(self):
        for _ in range(self.messages):
            self.module_input_queues['0'].put('x')
        self.module_input_queues['0'].put('kill')
        gevent.joinall(self.backgrounds)
        
class setupTest():
    '''
    Compare speed of direct queue to queue connections vs. 1 big queue with routing logic.
    
    '''
    
    def __init__(self):
        pass
    
    def test_1(self):
        '''Setup a classic Wisbone style set of 4 connected modules and push 50000 messages through them.'''
        setup = WishboneIO(jumps=4, messages=50000).go()
    
    def test_2(self):
        '''Use 1 big queue with routing logic for 4 connected modules and push 50000 messages through them.'''
        setup = RouterIO(jumps=4,messages=50000).go()


if __name__ == '__main__':
    instance=setupTest()
    test_lap=TestLap(instance=instance, iterations=1)
    test_lap.go()
