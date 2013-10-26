#!/usr/bin/python

from testlap import TestLap
from gevent import sleep

class DictionaryMethods():
    '''
    Figure out the fastest way to execute a function endlessly and do a gevent context switch every X cycle.
    '''

    def __init__(self, counter=100):
        self.counter=counter

    def executeMe(self):
        pass

    def test_1(self):
        '''Using a simple counter.'''

        x=0
        while True:
            if x == self.counter:
                break
            else:
                x+=1
                self.executeMe()

    def test_2(self):
        '''Using itertools.'''

        while True:
            for fc in [ self.executeMe for _ in xrange(self.counter) ] + [sleep]:
                fc()
            break

if __name__ == '__main__':
    instance=DictionaryMethods()
    test_lap=TestLap(instance=instance, iterations=1000000)
    test_lap.go()
