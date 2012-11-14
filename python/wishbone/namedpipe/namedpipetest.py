#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  namedpipetest.py
#  
#  Copyright 2012 Jelle Smet development@smetj.net
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

from wishbone import Wishbone
from wishbone.server import ParallelServer
from logging import DEBUG, INFO
import argparse

class NamedPipeTest():
    '''
    Description:
    
        This WishBone setup starts a named pipe listener.
        It accepts incoming data and print it on STDOUT.
    
        The module parameters can adapted in namedpipe.cfg.
    
    Goal:
    
        A demonstration of a named pipe listener.
    
    Usage:
    
        ./namedpipetest.py debug --config namedpipetest.cfg
    '''
    
    def __init__(self, namedpipe, stdout):
        self.namedpipe=namedpipe
        self.stdout=stdout
        self.setup()    

    def setup(self):
        wb = Wishbone()
        wb.registerModule ( ('wishbone.io_modules.namedpipe', 'NamedPipe', 'namedpipe'), **self.namedpipe )
        wb.registerModule ( ('wishbone.modules.stdout', 'STDOUT', 'stdout'), **self.stdout )
        
        #Connecting the dots
        wb.connect (wb.namedpipe.inbox, wb.stdout.inbox)
        wb.start()
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs=1, help='Which command to issue.  start, stop, status or debug.')
    parser.add_argument('--config', dest='config', help='The location of the configuration file.')
    parser.add_argument('--instances', dest='instances', default=1, help='The number of parallel instances to start.')
    parser.add_argument('--pid', dest='pid', default=1, help='The absolute path of the pidfile.')
    cli=vars(parser.parse_args())
    
    ParallelServer( instances=int(cli['instances']),
                    setup=NamedPipeTest,
                    command=cli['command'][0],
                    config=cli['config'],
                    name='NamedPipeTest',
                    log_level=DEBUG
    )

if __name__ == '__main__':
    main()
