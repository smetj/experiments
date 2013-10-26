#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  dictvsclass.py
#
#  Copyright 2013 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


from testlap import TestLap
from random import randint

class DataStructure1():
    def __init__(self, one, two, three):
        self.one=one
        self.two=two
        self.three=three

class DataStructure2():
    one=None
    two=None
    three=None

class DictVSClass():
    '''Check speed of data structure creation.'''

    def __init__(self):
        pass

    def test_1(self):
        '''Class store 3 values during init.'''
        a=DataStructure1(1,2,3)

    def test_2(self):
        '''Class store 3 values after init.'''
        a=DataStructure2()
        a.one=1
        a.two=2
        a.three=3

    def test_3(self):
        '''Dictionary to store 3 values.'''
        a={"one":1,"two":2,"three":3}



if __name__ == '__main__':
    instance=DictVSClass()
    test_lap=TestLap(instance=instance, iterations=10000000)
    test_lap.go()
