#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  looping_threading.py
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

import threading
from sys import stdout
from time import sleep

class looper0(threading.Thread):
    def run(self):
        while True:
            for _ in range(100):
                stdout.write ("0")

class looper1(threading.Thread):
    def run(self):
        while True:
            for _ in range(100):
                stdout.write ("1")                
            
def main():
    looper0().start()
    looper1().start()
    #sleep(10)
    

if __name__ == '__main__':
	main()

