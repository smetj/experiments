#!/usr/bin/python

from testlap import TestLap
import sys
import socket

class OutputData():
    '''
    Compare speed of writing data to a remote UDP listener using 2 different methods:
        * Write to stdout/stderr and pipe to remote listener using netcat
        * Write directly to the remote listener
    
    Start in another shell a listening UDP server which writes data to /dev/null:
        
        $ nc -klu localhost 10000 > /dev/null
        
    Start this script by redirecting STDERR to a nc process:
    
        $ python compare_stdout_socket.py 2> >(nc -w1 -u localhost 10000)
        
    '''

    def __init__(self,size=1):
        self.dictionary={"one":1}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.size=size

    def test_1(self):
        '''Write to STDERR so we can redirect this output and keep the TestLap summary on STDOUT.'''
        sys.stderr.write("x"*self.size)
    
    def test_2(self):
        '''Write directly to a remote socket.'''
        self.socket.sendto("x"*self.size,('127.0.0.1',10000))
    
    def end_test_2(self):
        self.socket.close()

if __name__ == '__main__':
    instance=OutputData(size=8192)
    test_lap=TestLap(instance=instance, iterations=1000000)
    test_lap.go()
