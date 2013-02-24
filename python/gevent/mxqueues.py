#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mxqueues.py
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

#import uvent
#uvent.install()
from gevent import spawn, sleep, monkey
from gevent.event import Event
from sys import stdout
from mx.Queue import Queue
from gevent import Greenlet
monkey.patch_all()

class Shuffler(Greenlet):
    def __init__(self,name):
        Greenlet.__init__(self)
        self.name=name
        self.inbox=Queue()
        self.outbox=Queue()
        self.proceed=Event()
        self.proceed.set()
        
    def _run(self):
        while True:
            while self.switcher():
                doc = self.inbox.pop()
                print ("%s: got element"%self.name)
                self.outbox.push(doc)
            sleep(0.1)
    
    def switcher(self):
        sleep(0)
        if self.inbox:
            return True
        else:
            return False

class Connector(Greenlet):
    def __init__(self, consume, produce):
        Greenlet.__init__(self)
        self.consume=consume
        self.produce=produce
        self.proceed=Event()
        self.proceed.set()
    def _run(self):
        while True:
            while self.switcher():
                doc = self.consume.pop()
                print ("Connector: got element")
                self.produce.push(doc)
            sleep(0.1)
    
    def switcher(self):
        sleep(0)
        if self.consume:
            return True
        else:
            return False
    
    

def main():
    one=Shuffler("one")
    two=Shuffler("two")
    connector=Connector(one.outbox,two.inbox)

    for _ in range(100):
        one.inbox.push("x")
    
    connector.start()
    two.start()
    one.start()
    while True:
        sleep(1)  
    

if __name__ == '__main__':
	main()
