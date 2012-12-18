#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mod_gearman.py
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

import gearman
import gevent
import base64
import time
from gevent import monkey
from Crypto.Cipher import AES
monkey.patch_all()

class GearmanPerfData():
    
    def __init__(self, secret):
        self.cipher=AES.new(secret[0:32])
        self.start=time.time()
        self.counter=0

    def decode(self, data):
        return self.cipher.decrypt(base64.b64decode(data))

    def getData(self, gearman_worker, gearman_job):
        print (self.decode(gearman_job.data))
        self.counter+=1
        return gearman_job.data

class CustomGearmanWorker(gearman.GearmanWorker):

    def __init__(self,*args,**kwargs):
        self.max_jobs=kwargs.get('max_jobs',100)
        del kwargs['max_jobs']
        self.counter=0
        self.cont=True
        gearman.GearmanWorker.__init__(self,*args,**kwargs)

    def on_job_execute(self, current_job):
        if self.counter >= self.max_jobs:
            self.cont=False
        self.counter+=1        
        return super(CustomGearmanWorker, self).on_job_execute(current_job)

    def work(self, poll_timeout=60):
        
        """Loop indefinitely, complete tasks from all connections."""
        
        continue_working = True
        worker_connections = []

        def continue_while_connections_alive(any_activity):
            return self.after_poll(any_activity)

        while continue_working and self.cont==True:
            worker_connections = self.establish_worker_connections()
            continue_working = self.poll_connections_until_stopped(worker_connections, continue_while_connections_alive, timeout=poll_timeout)

        for current_connection in worker_connections:
            current_connection.close()

    def after_poll(self, any_activity):
        return self.cont

class setupWorker():

    def __init__(self):        
        #self.worker=CustomGearmanWorker(['besrvuc-nag02.ttg.global:4730'],max_jobs=1)
        self.worker=gearman.GearmanWorker(['besrvuc-nag02.ttg.global:4730'])
        self.perfdata = GearmanPerfData(secret='Aloh9uibshojeF8oAhyo3eefGu5ohr3iDeek4ehamaM9eisoas6OoveiareQuo0i')
        self.worker.register_task('perfdata', self.perfdata.getData)
        
    def go(self):
        self.worker.work()    

def main():
    instance=[]
    background=[]
    for _ in range(50):
        instance.append(setupWorker())
        background.append(gevent.spawn(instance[-1].go()))
        
    while True:
        gevent.sleep(1)
        
        

if __name__ == '__main__':
    main()

