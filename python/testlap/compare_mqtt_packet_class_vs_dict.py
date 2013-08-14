#!/usr/bin/python

from testlap import TestLap
from random import randint
from mosquitto import MosquittoInPacket

class PacketClassVSDict():
    '''
    Figure out the init speed impact of using a class VS dict as incoming packet representation.
    '''

    def __init__(self):
        pass

    def test_1(self):
        '''Use the MosquittoInPacket class for packet representation.'''

        packet = MosquittoInPacket()

    def test_2(self):
        '''Use a dict for packet representation.'''

        packet = { "command":0,
            "have_remaining":0,
            "remaining_count":[],
            "remaining_mult":1,
            "remaining_length":0,
            "packet" :b"",
            "to_process":0,
            "self.pos":0}

if __name__ == '__main__':
    instance=PacketClassVSDict()
    test_lap=TestLap(instance=instance, iterations=10000000)
    test_lap.go()
