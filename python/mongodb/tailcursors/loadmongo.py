#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  loadmongo.py
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

import logging
from wishbone.toolkit import QueueFunctions, Block
from gevent import Greenlet, spawn, sleep
import pymongo
from gevent import monkey;monkey.patch_all()

class LoadMongo(Greenlet, QueueFunctions, Block):
    '''**A Wishbone IO which loads messages into a MongoDB capped collection.**
            
    Parameters:        

        - name (str):           The instance name when initiated.
        - host (str):           The name or IP of MongoDB.
        - db (str):             The name of the database.
        - collection (str):     The name of the collection.
        - capped (bool):        Whether the collection is capped.
        - size (int):           Maximum size of the capped collection.
        - max (int):            Maximum number of documents in the capped collection.

    Queues:
        
        - outbox:               Messages destined for MongoDB.
    '''
    
    def __init__(self, name, host, db, collection, capped=False, size=100000,max=100000):
        Greenlet.__init__(self)
        Block.__init__(self)
        QueueFunctions.__init__(self)
        self.name=name
        self.logging = logging.getLogger( self.name )
        self.logging.info('Initiated')
        self.host=host
        self.db=db
        self.collection=collection
        self.capped=capped
        self.size=size
        self.max=max
        self.collection = self.__setup()

    def __setup(self):
        '''Creates the capped collection if required.
        '''
        connection = pymongo.MongoClient(self.host)
        db = connection[self.db]
        try:
            db.create_collection(self.collection, capped=self.capped, size=self.size, max=self.max)
        except:
            self.logging.info("Collection %s already exits."%(self.collection))
        return db[self.collection]
        
                                
    def _run(self):
        '''
        Blocking function which consumes self.outbox and writes the data to the capped collection.
        '''
        
        self.logging.info('Started')
        while self.block() == True:
            self.collection.insert(self.outbox.get())
            self.logging.debug('Inserted document in collection.')

    def shutdown(self):
        pass
