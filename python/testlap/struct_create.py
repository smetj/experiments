#!/usr/bin/python

from testlap import TestLap
import struct

class StructCompare():
    '''
    Checks whether base matters when using struct.
    '''

    def __init__(self):
        pass

    def test_1(self):
        '''Integer'''

        a=bytearray()
        for _ in xrange(1000000):
            a.extend(struct.pack("!B",1))

    def test_2(self):
        '''Hex.'''

        a=bytearray()
        for _ in xrange(1000000):
            a.extend(struct.pack("!B",0b1))

    def test_3(self):
        '''Binary.'''

        a=bytearray()
        for _ in xrange(1000000):
            a.extend(struct.pack("!B",0x1))


if __name__ == '__main__':
    instance=StructCompare()
    test_lap=TestLap(instance=instance, iterations=100)
    test_lap.go()
