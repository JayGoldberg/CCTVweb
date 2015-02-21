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

filepath = sys.argv[1]

if os.path.exists(filepath):
  print('Opening file %s' % filepath)

  # TODO: put this in a try block
  f = open(filepath)
  reader = csv.reader(f)

  # TODO: define DB settings in config file
  print('Connecting to DB')
  client = MongoClient()
  db = client.mydb
  collection = db.images
  print('Connected to DB')
  
  collection.drop()
  
  print('Building insert data')
  bulk_data = []
  for row in reader:
      path = row[0] # the first element is always the path
      decoded = json.loads(row[1]) # parse the json field in the CSV
      
      new_record = {"path": path,
             "IQimage": decoded['IQimage']}
      bulk_data.append(new_record)
  
  print('Beginning insert')
  collection.insert(bulk_data)
  print('Finished insert')
  
  f.close()
  
else:
  print('File does not exist')
