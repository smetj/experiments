#!/usr/bin/python

from testlap import TestLap
import gevent
from gevent import Greenlet
from gevent.queue import Queue
import zmq.green as zmq

# GeventQueues
###############
class GeventQueues():
    def __init__(self,number=100000):
        thread1 = WishboneBasedActor()
        thread2 = WishboneBasedActor()
        for _ in range(number):
            thread1.inbox.put("x")
        shuffle = gevent.Greenlet.spawn(self.shuffler,thread1.outbox,thread2.inbox)
        thread1.start()
        thread2.start()

        while True:
            if thread2.outbox.qsize() == number:
                break
            else:
                gevent.sleep(0.1)
    def shuffler(self,inbox,outbox):
        while True:
            message = inbox.get()
            outbox.put(message)
            gevent.sleep()

class WishboneBasedActor(Greenlet):
    '''An Wishbone style actor shuffling Gevent Queues'''

    def __init__(self):
        Greenlet.__init__(self)
        self.inbox = Queue(None)
        self.outbox = Queue(None)
    def _run(self):
        while True:
            message = self.inbox.get()
            self.outbox.put(message)
            gevent.sleep()

# ZMQIPCQueues
##############
class ZMQIPC():
    def __init__(self,number=100000):
        self.context = zmq.Context()
        thread1 = ZMQIPCActor("one",self.context)
        thread2 = ZMQIPCActor2("two",self.context,number=number)
        self.dumpData(number)
        shuffle = gevent.Greenlet.spawn(self.shuffler,"one.outbox","two.inbox")
        thread1.start()
        thread2.start()

        thread2.block.wait()

    def dumpData(self,number):
        dumper = self.context.socket(zmq.PUSH)
        dumper.connect("inproc://%s"%("one.inbox"))
        for _ in range(number):
            dumper.send("x")
        dumper.send("y")

    def shuffler(self,inbox,outbox):
        inb = self.context.socket(zmq.PULL)
        inb.connect("inproc://%s"%(inbox))
        outb = self.context.socket(zmq.PUSH)
        outb.connect("inproc://%s"%(outbox))
        while True:
            message = inb.recv()
            outb.send(message)

class ZMQIPCActor(Greenlet):
    '''An actor shuffling ZeroMQ Queues'''

    def __init__(self,name,context):
        Greenlet.__init__(self)
        self.name=name
        self.context = context
        self.inbox = self.context.socket(zmq.PULL)
        self.inbox.bind("inproc://%s.inbox"%(name))
        self.outbox = self.context.socket(zmq.PUSH)
        self.outbox.bind("inproc://%s.outbox"%(name))

    def _run(self):
        while True:
            data = self.inbox.recv()
            #print "%s:%s"%(self.name,data)
            self.outbox.send(data)
            gevent.sleep()

class ZMQIPCActor2(Greenlet):
    '''An actor shuffling ZeroMQ Queues.  Does write into outbox since nobody listens
    on that it blocks.'''

    def __init__(self,name,context,number):
        Greenlet.__init__(self)
        self.name=name
        self.context = context
        self.number = number
        self.inbox = self.context.socket(zmq.PULL)
        self.inbox.bind("inproc://%s.inbox"%(name))
        self.outbox = self.context.socket(zmq.PUSH)
        self.outbox.bind("inproc://%s.outbox"%(name))
        self.block=gevent.event.Event()
        self.block.clear()

    def _run(self):
        counter=0
        while True:
            data = self.inbox.recv()
            counter+=1
            if counter == self.number:
                self.block.set()
                break
            gevent.sleep()

# ZMQPUBSUB
###########

class ZMQPUBSUB():
    def __init__(self,number=10):
        self.number=number
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:10000")
        thread1 = ZMQPUBSUBActor("one",self.context,"two.inbox")
        thread2 = ZMQPUBSUBActor("two",self.context)
        self.dump()
        thread1.start()
        thread2.start()
        
        while True:
            gevent.sleep(0.1)
            
    def dump(self):
        for _ in range(self.number):
            self.socket.send("one.inbox x")
        
class ZMQPUBSUBActor(Greenlet):
    
    def __init__(self,name,context,topic=None):
        self.name=name
        self.topic=topic
        Greenlet.__init__(self)
        
        self.inbox=context.socket(zmq.SUB)
        self.inbox.setsockopt(zmq.SUBSCRIBE, "%s.inbox"%(name))
        self.inbox.connect("tcp://*:10000")
        
        self.outbox=context.socket(zmq.PUB)
        self.outbox.connect("tcp://*:10000")
        
    def _run(self):
        while True:
            message = self.inbox.recv()
            #print message
            #print "%s %s"%(self.name,message)
            if self.topic != None:
                (topic, data)=message.split()
                print "sending %s %s"%(self.topic, data)
                self.outbox.send("%s %s"%(self.topic, data))
    
class MessagePassing():
    '''Compare the speed of passing messages between 2 greenthreads using gevent queues or zmq sockets.'''

    def __init__(self):
        pass

    def test_1(self):
        '''Emulate Wishbone's way of suffling messages from 1 greenthread to another.'''
        GeventQueues()
    
    def test_2(self):
        '''ZMQ IPC style queues/sockets.'''
        ZMQIPC()

    def zeromqSockets(self):
        pass

if __name__ == '__main__':
    ZMQPUBSUB()
    #instance=MessagePassing()
    #test_lap=TestLap(instance=instance, iterations=1)
    #test_lap.go()
