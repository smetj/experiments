#!/usr/bin/python

from testlap import TestLap
from wishbone.tools import WishboneQueue

class QueueSizeEval():
    '''
    Measure the pentalty when evaluating the maximum size of a queue.
    '''

    def __init__(self):
        pass

    def test_1(self):
        '''No evaluation'''
        q = WishboneQueue()

        for _ in xrange(1000000):
            q.put(1)

    def test_2(self):
        '''With evaluation'''

        q = WishboneQueue(max_size=1000001)

        for _ in xrange(1000000):
            q.put(1)

if __name__ == '__main__':
    instance=QueueSizeEval()
    test_lap=TestLap(instance=instance, iterations=10)
    test_lap.go()
