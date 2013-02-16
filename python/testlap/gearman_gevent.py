#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gearman_gevent_speed_test.py
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
import gearman
from gevent import monkey

class CustomGearmanWorker(gearman.GearmanWorker):

    def __init__(self,*args,**kwargs):
        self.max_jobs=kwargs.get('max_jobs',100)
        del kwargs['max_jobs']
        self.counter=1
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


class GearmanIO():
    def __init__(self,gm_server,jobs=100,data="This is a test"):
        self.gm_server=gm_server
        self.jobs=jobs
        self.data=data
        
    def test_1(self):
        '''Submit to job queue without gevent.'''
        
        gm_client = gearman.GearmanClient([self.gm_server])
        for _ in range(self.jobs):            
            gm_client.submit_job("without_gevent",self.data,background=True)
    
    def test_2(self):
        '''Retrieve from job queue without gevent.'''
        def do(worker, job):
            return job.data
        worker=CustomGearmanWorker([self.gm_server],max_jobs=self.jobs)
        worker.register_task('without_gevent', do)
        worker.work()

    def test_3(self):
        '''Submit to job queue with gevent.'''
        
        monkey.patch_all()
        gm_client = gearman.GearmanClient([self.gm_server])
        for _ in range(self.jobs):            
            gm_client.submit_job("with_gevent",self.data,background=True)
    
    def test_4(self):
        '''Retrieve from job queue with gevent.'''
        
        #monkey.patch_all()
        def do(worker, job):
            return job.data
        worker=CustomGearmanWorker([self.gm_server],max_jobs=self.jobs)
        worker.register_task('with_gevent', do)
        worker.work()

if __name__ == '__main__':
    instance=GearmanIO('sandbox',jobs=10,threads=10,data="gearman_gevent")
    test_lap=TestLap(instance=instance, iterations=1)
    test_lap.go()
