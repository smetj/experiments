#!/usr/bin/python

import timeit
import sys
import platform
from prettytable import PrettyTable
from testlap import TestLap

class DictionaryMethods():
    '''
    Verify an existing key in a dictionary.
    '''

    def __init__(self):
        self.dictionary={"one":1}

    def test_1(self):
        '''Check if an existing key exists in dictionary using has_key.'''

        if self.dictionary.has_key('one'):
            return True
        else:
            return False

    def test_2(self):
        '''Check if an non existing key exists in dictionary using has_key.'''

        if self.dictionary.has_key('two'):
            return True
        else:
            return False

    def test_3(self):
        '''Check if an existing key exists in dictionary using try except.'''
        try:
            self.dictionary["one"]
            return True
        except:
            return False

    def test_4(self):
        '''Check if a non existing key exists in dictionary using try except.'''
        try:
            self.dictionary["two"]
            return True
        except:
            return False

    def test_5(self):
        '''Check if an existing key exists in dictionary using try except KeyError.'''
        try:
            self.dictionary["two"]
            return True
        except KeyError:
            return False

    def test_6(self):
        '''Check if an existing key exists in dictionary using in syntax.'''
        if 'one' in self.dictionary:
            return True
        else:
            return False

    def test_7(self):
        '''Check if a non existing key exists in dictionary using in syntax.'''
        if 'two' in self.dictionary:
            return True
        else:
            return False


if __name__ == '__main__':
    instance=DictionaryMethods()
    test_lap=TestLap(instance=instance, iterations=10000000)
    test_lap.go()
