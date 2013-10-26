#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  poly.py
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

class PolyCompare():
    '''
    Check how if/then compares to getattr
    '''

    def __init__(self):
        pass

    def number_0(self):
        pass

    def number_1(self):
        pass

    def test_1(self):
        '''Choose definition to execute with using if/then.'''

        for _ in xrange(1000000):
            function = randint(0,1)
            if function == 0:
                self.number_0()
            elif function == 1:
                self.number_1()

    def test_2(self):
        '''Choose definition to execute with getattr.'''

        for _ in xrange(1000000):
            getattr(self, "number_%s"%(randint(0,1)))()

if __name__ == '__main__':
    instance=PolyCompare()
    test_lap=TestLap(instance=instance, iterations=10)
    test_lap.go()
