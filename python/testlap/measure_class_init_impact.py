#!/usr/bin/python

from testlap import TestLap
from random import randint

class SomeClass():
    def __init__(self):
        pass
    def go(self):
        pass

class ValueEvaluation():
    '''
    Figure out whether initializing a class is expensive.
    '''

    def __init__(self):
        pass

    def someFunction(self):
        pass

    def test_1(self):
        '''Just call a local function.'''
        
        self.someFunction()

    def test_2(self):
        '''Initialize a class and call a function from it.'''
        
        test=SomeClass()
        test.go()

if __name__ == '__main__':
    instance=ValueEvaluation()
    test_lap=TestLap(instance=instance, iterations=10000000)
    test_lap.go()
