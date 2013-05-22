#!/usr/bin/python

from testlap import TestLap
from collections import deque
from Queue import Queue as python_queue
from mx.Queue import Queue as mx_queue
from mx.Stack import Stack as mx_stack

class QueueCompare():
    '''
    Compare IO speed of different queue implementations.

    Pushing and popping 1000000 integers.
    '''

    def __init__(self, number=1000000):
        self.mx_queue = mx_queue()
        self.mx_stack = mx_stack()
        self.python_queue = python_queue()
        self.deque = deque()
        self.number=number

    def test_1_mx_queue_push(self):
        '''Push to mx queue'''

        for x in xrange(self.number):
            self.mx_queue.push(x)

    def test_2_mx_queue_pop(self):
        '''Pop from mx queue'''

        for x in xrange(self.number):
            self.mx_queue.pop()

    def test_3_mx_stack_push(self):
        '''Push to mx stack'''

        for x in xrange(self.number):
            self.mx_stack.push(x)

    def test_4_mx_stack_pop(self):
        '''Pop from mx stack'''

        for x in xrange(self.number):
            self.mx_stack.pop()

    def test_5_python_queue_push(self):
        '''Push to python queue.'''

        for x in xrange(self.number):
            self.python_queue.put(x)

    def test_6_python_queue_pop(self):
        '''Pop from python queue'''

        for x in xrange(self.number):
            self.python_queue.get()

    def test_7_deque_push(self):
        '''Push to python deque.'''

        for x in xrange(self.number):
            self.deque.append(x)

    def test_8_deque_pop(self):
        '''Pop from python deque'''

        for x in xrange(self.number):
            self.deque.popleft()

if __name__ == '__main__':
    instance=QueueCompare()
    test_lap=TestLap(instance=instance, iterations=1)
    test_lap.go()
