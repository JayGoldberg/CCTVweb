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
  def __init__(self, numlines_per_chunk):
    self.chunksize = numlines_per_chunk
    self.iterator = 0
    self.chunk = []
    self.progress = 0
      
  def addline(self, line):
    if self.iterator < self.chunksize:
      self.chunk.append(line)
      self.iterator += 1
    else:
      # we are missing files at the end
      print("Commit!")
      self.mongocommit()
      self.chunk.append(line)
      self.iterator += 1

  def mongocommit(self):
    #print('Beginning insert')
    bulk_data = []
    for i in self.chunk:
      pair = i.split(',', 1)
      path = pair[0] # the first element is always the path
      decoded = json.loads(pair[1]) # parse the json field in the CSV
      new_record = {"path": path,
              "IQimage": decoded['IQimage']}
      bulk_data.append(new_record)

    collection.insert(bulk_data)
    #print('Finished insert')
    self.iterator = 0
    self.chunk = []
    self.progress += 1
    print(self.progress * self.chunksize)
      
  def complete(self):
    collection.create_index("IQimage.time", pymongo.ASCENDING)

filepath = sys.argv[1]

mongochunker = Importer(5000)

if os.path.exists(filepath):
  print('Opening file %s' % filepath)

  # TODO: put this in a try block
  f = open(filepath)

  # TODO: define DB settings in config file
  print('Connecting to DB')
  client = MongoClient()
  db = client.mydb
  collection = db.images
  print('Connected to DB')
  print('Drop collection')
  
  collection.drop()
  
  print('Read input data')
  
  for line in f:
    mongochunker.addline(line)
  f.close()
  
  print("Building index")
  
else:
  print('File does not exist')
