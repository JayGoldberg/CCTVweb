#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"
__status__ = "Alpha"

import os, sys, csv, json, datetime
import pymongo
from pymongo import MongoClient

class Importer:
  def __init__(self, numlines_per_chunk, totallines):
    self.chunksize = numlines_per_chunk # how many lines to read, and insert at a time
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
    for i in self.chunk:
      pair = i.split(',', 1)
      path = pair[0] # the first element is always the path
      decoded = json.loads(pair[1]) # parse the json field in the CSV
      new_record = {"path": path,
              "IQimage": decoded['IQimage']}
      bulk_data.append(new_record)

    collection.insert(bulk_data)
    recordsdone = self.progress * self.chunksize
    print("Committed " + str(recordsdone) + " records. " + "{0:.0f}%".format((float(recordsdone)/self.totallines) * 100))
    self.iterator = 0
    self.chunk = []
    self.progress += 1
      
  def complete(self):
    self.mongocommit()
    collection.create_index("IQimage.time", pymongo.ASCENDING)

camname = sys.argv[1]
filepath = sys.argv[2]

if os.path.exists(filepath):
  print('Opening file %s' % filepath)

  # TODO: put this in a try block
  f = open(filepath)
  
  for lineno, content in enumerate(f):
    pass
  
  f.seek(0)
  
  # specify chunksize and total length
  mongochunker = Importer(10000, lineno+1)

  # TODO: define DB settings in config file
  print('Connecting to DB')
  client = MongoClient('mongodb://localhost:27017/')
  db = client.mydb
  collection = db[camname]
  print('Connected to DB')
  print('Drop collection')
  
  collection.drop()
  
  print('Read input data')
  
  for line in f:
    mongochunker.addline(line)
  f.close()
  
  print("Building index")
  mongochunker.complete()
  print("Built index")
  
else:
  print('File does not exist')
