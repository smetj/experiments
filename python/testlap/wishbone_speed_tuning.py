#!/usr/bin/python

from testlap import TestLap
from gevent.queue import Queue as gevent_queue
from mx.Queue import Queue as mx_queue

class QueueShuffling():
    '''Verify possible speed tuning with different message shuffling scenarios.'''

    def __init__(self,messages=10000000):
        self.queue1 = self.getGeventQueue(messages,"x")
        #self.queue2 = self.getGeventQueue(messages,"x")
        self.queue3 = self.getMXQueue(messages,"x")
    
    def getGeventQueue(self, number, element):
        '''Prepare a Gevent queue with number elements.  It is not part of the speed measurements.'''
        print ("preparing Queue")
        queue=gevent_queue()
        for _ in range(number):
            queue.put(element)
        print ("Done")
        return queue

    def getMXQueue(self, number, element):
        '''Prepare a MX queue with number elements.  It is not part oc the speed measurements.'''
        print ("preparing Queue")
        queue=mx_queue()
        for _ in range(number):
            queue.push(element)
        print ("Done")
        return queue

    def test_1(self):
        '''Consume a Gevent queue using True'''
        
        while True:
            try:
                self.queue1.get()
            except:
                break

    def xtest_2(self):
        '''Consume a Gevent queue using 1'''
        
        while 1:
            try:
                self.queue2.get()
            except:
                break
    
    def test_3(self):
        '''Consume a MX queue using True'''
        
        while True:
            while self.queue3:
                self.queue3.pop()
            break

                
if __name__ == '__main__':
    instance=QueueShuffling()
    test_lap=TestLap(instance=instance, iterations=1)
    test_lap.go()
