#!/usr/bin/python

from testlap import TestLap
import random

class ConditionalFunctionExecution():
    '''
    Compare the difference in speed between evaluating a condition or using a
    has reference to execute a function.

    '''

    def __init__(self):
        self.lookup={1: self.doOne, 2: self.doTwo, 3: self.doThree, 4: self.doFour}

    def test_1(self):
        '''Using a condition'''

        number = random.randint(1,4)
        if  number == 1:
            self.doOne()
        elif number == 2:
            self.doTwo()
        elif number == 3:
            self.doThree()
        else:
            self.doFour()

    def test_2(self):
        '''Using a hashmap'''

        self.lookup[random.randint(1,4)]()

    def doOne(self):
        pass

    def doTwo(self):
        pass

    def doThree(self):
        pass

    def doFour(self):
        pass


if __name__ == '__main__':
    instance=ConditionalFunctionExecution()
    test_lap=TestLap(instance=instance, iterations=10000000)
    test_lap.go()
