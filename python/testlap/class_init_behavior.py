#!/usr/bin/python

from testlap import TestLap

class BaseFunctions():
    def xdo(self,data):
        return data+"x"
    
    def ydo(self,data):
        return data+"y"
    
    def zdo(self,data):
        return data+"z"
    
class BuildClassGetattr(BaseFunctions):
    
    def __init__(self,execute):
        self.execute=execute
    
    def do(self,data):
        for definition in self.execute:
            data = getattr(self,definition)(data)
        return data
        
class BuildClassConditionals(BaseFunctions):
    
    def __init__(self,xdo=False,ydo=False,zdo=False):
        self.x=xdo
        self.y=ydo
        self.z=zdo
    
    def do(self,data):
        if self.x:
            data = self.xdo(data)
        if self.y:
            data = self.ydo(data)
        if self.z:
            data = self.zdo(data)
        return data
        
class BuildClassExec(BaseFunctions)
    
    def __init__(self, 


class ClassBehaviour():
    '''
    Comparing speed of different approaches to determine the class functionality on class init.
    '''

    def __init__(self,iterations):
        self.iterations=iterations

    def test_1(self):
        '''A list containing the functions to execute.'''
        
        test1=BuildClassGetattr([ "xdo","ydo","zdo" ])
        for _ in range(self.iterations):
            test1.do("ABC")

    def test_2(self):
        '''Using conditionals to determine what to execute.'''

        test2=BuildClassConditionals(xdo=True,ydo=True,zdo=True)
        for _ in range(self.iterations):
            test2.do("ABC")


if __name__ == '__main__':
    instance=ClassBehaviour(10000)
    test_lap=TestLap(instance=instance, iterations=1)
    test_lap.go()
