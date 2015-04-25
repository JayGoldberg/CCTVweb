#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "MIT"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

import os, sys, csv, json, datetime
import pymongo
from pymongo import MongoClient

filepath = sys.argv[1]

if os.path.exists(filepath):
  print('Opening file %s' % filepath)

  # TODO: put this in a try block
  f = open(filepath)
  #reader = csv.reader(f, quotechar='{', quoting=csv.QUOTE_MINIMAL)

  # TODO: define DB settings in config file
  print('Connecting to DB')
  client = MongoClient()
  db = client.mydb
  collection = db.images
  print('Connected to DB')
  
  print('Building insert data')
  bulk_data = []
  #for row in reader:
  #    print(row[1])
  #    path = row[0] # the first element is always the path
  #    decoded = json.loads(row[1]) # parse the json field in the CSV
  #    
  #    new_record = {"path": path,
  #           "IQimage": decoded['IQimage']}
  #    bulk_data.append(new_record)
  
  records = []
  for line in f:
      records.append(line.split(',', 1))

  for pair in records:
      path = pair[0] # the first element is always the path
      decoded = json.loads(pair[1]) # parse the json field in the CSV

      new_record = {"path": path,
           "IQimage": decoded['IQimage']}
      bulk_data.append(new_record)
      
  collection.drop()
  
  print('Beginning insert')
  for i in range(0, len(bulk_data), 2000):
      collection.insert(bulk_data[i:i+2000])
      print(i) # progress indicator
  print('Finished insert')
  
  f.close()

  # this doesn't seem to work right now. Run manually in mongo with 'db.images.createIndex( { "IQimage.time": 1 } )'
  print("Building index")
  collection.create_index("IQimage.time", pymongo.ASCENDING)
  
else:
  print('File does not exist')
