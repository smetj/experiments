#!/usr/bin/python

from testlap import TestLap
from random import randint

class ValueEvaluation():
    '''
    Compare if then against try: except.
    '''

    def __init__(self):
        pass

    def test_1(self):
        '''Evaluate a value using if then else.'''
        
        number = randint(0,1)
        if number == 1:
            pass
        else:
            pass

    def test_2(self):
        '''Evaluate a value using try: except.'''

        number = randint(0,1)
        try:
            number == 1
        except:
            pass

if __name__ == '__main__':
    instance=ValueEvaluation()
    test_lap=TestLap(instance=instance, iterations=10000000)
    test_lap.go()
