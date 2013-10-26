#!/usr/bin/python

from testlap import TestLap

class ValueEvaluation():
    '''
    Compare using getattr against directly referring to a method.
    '''

    def __init__(self):
        self.value="hello"

    def test_1(self):
        '''Reference using getattr'''

        getattr(self, 'value')

    def test_2(self):
        '''Reference directly'''

        self.value

if __name__ == '__main__':
    instance=ValueEvaluation()
    test_lap=TestLap(instance=instance, iterations=10000000)
    test_lap.go()
