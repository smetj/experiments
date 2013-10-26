#!/usr/bin/env pythoni
# -*- coding: utf-8 -*-
#
#  untitled.py
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

import zmq.green as zmq
from gevent import Greenlet
from gevent import sleep
from gevent import monkey
from time import time
monkey.patch_all(time=True)


class Actor(Greenlet):
    '''Context is created inside class'''
    
    def __init__(self, name, out, socket, context):
        Greenlet.__init__(self)
        self.name=name
        self.out=out
        self.counter=0

        self.context=context
                
        self.inbox=self.context.socket(zmq.SUB)
        self.inbox.connect("inproc://test")
        self.inbox.setsockopt(zmq.SUBSCRIBE, name)        
        
        self.outbox=socket
        
    def _run(self):
        while True:
            (topic, data)=self.inbox.recv().split()
            self.counter+=1
            #print "%s: %s"%(self.out,data)
            self.outbox.send("%s %s"%(self.out, data))

def main():
    context=zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("inproc://test")
      
    one=Actor("one","two",socket, context)
    two=Actor("two","one",socket, context)
    one.start()
    two.start()
    sleep(1)
    
    socket.send("one 1")
    
    prev_c=two.counter
    prev_t=time()
    while True:
        now_c=two.counter
        now_t=time()
        print (now_c-prev_c)/(now_t-prev_t)
        prev_c=now_c
        prev_t=now_t
        
        
        sleep(1)
    
if __name__ == '__main__':
    main()
