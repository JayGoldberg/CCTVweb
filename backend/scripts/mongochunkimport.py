#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "Apache 2.0"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

import pymongo
from pymongo import MongoClient

class MongoChunkImport:
    def __init__(self, chunksize=None, totallines=None, dbname=None, collection=None):
        client = MongoClient('mongodb://localhost:27017/')

        if not collection or not dbname:
           print("MongoChunkImport requires a db and collection argument")
        else:
          db = client[dbname]
          self.collection = db[collection]

        self.collection.drop() # TODO: well that's dangerous to do before you know if
                               # the rest of the operation will succeed

        self.chunksize = chunksize # how many lines to read, and insert at a time
        self.iterator = 0
        self.chunk = []
        self.progress = 0
        self.totallines = totallines
      
    def addline(self, line):
        if self.iterator < self.chunksize:
            self.chunk.append(line)
            self.iterator += 1
        else:
            self.mongocommit()
            self.chunk.append(line)
            self.iterator += 1

    def mongocommit(self):
        bulk_data = []
        for record in self.chunk:
            bulk_data.append(record)

        self.collection.insert(bulk_data)
        recordsdone = self.progress * self.chunksize
        print("Committed " + str(recordsdone) + " records. " + "{0:.0f}%".format((float(recordsdone)/self.totallines) * 100))
        self.iterator = 0
        self.chunk = []
        self.progress += 1
      
    def close(self):
        self.mongocommit()
#       collection.create_index("IQimage.time", pymongo.ASCENDING)
