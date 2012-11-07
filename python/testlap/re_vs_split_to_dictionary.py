#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  re_vs_split_to_dictionary.py
#  
#  Copyright 2012 Jelle Smet <development@smetj.net>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
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
import re

class setupTest():
    
    '''This test is to get an idea what the performance impact is of using regular expressions compared to execute multiple string splits.'''
    
    def __init__(self):
        self.data="0=a 1=b 2=c 3=d 4=e 5=f 6=g 7=h 8=i 9=j"        
    
    def test_1(self):
        
        '''Use a regular expression to extract data.'''
        
        result={}
        for group in re.findall('(\d)=(\w)', self.data):
            result[group[0]]=group[1]
    
    def test_2(self):
        
        '''Use string split to extract data.'''
        
        result={}
        for group in self.data.split(' '):
            (a,b)=group.split('=')
            result[a]=b

if __name__ == '__main__':
    instance=setupTest()
    test_lap=TestLap(instance=instance, iterations=1000000)
    test_lap.go()
