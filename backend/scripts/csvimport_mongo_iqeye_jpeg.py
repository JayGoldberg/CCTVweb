#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "Apache 2.0"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

import os
import sys
import csv
import json

from mongochunkimport import MongoChunkImport

if __name__ == '__main__':
  dbname = sys.argv[1]
  camname = sys.argv[2]
  filepath = sys.argv[3]

  if os.path.exists(filepath):
    print('Opening file %s' % filepath)

    # TODO: put this in a try block
    f = open(filepath, 'r')
  
    for lineno, content in enumerate(f):
      pass
  
    f.seek(0)
  
    # specify chunksize and total length

    mongochunker = MongoChunkImport(chunksize=100, totallines=lineno+1, dbname=dbname, collection=camname) 
  
    for line in f:
      pair = line.split(',', 1)
      path = pair[0] # the first element is always the path
      decoded = json.loads(pair[1]) # parse the json field in the CSV
      new_record = {"path": path,
              "IQimage": decoded['IQimage']}  
      mongochunker.addline(new_record)
    f.close()
    
    mongochunker.close()
  
else:
  print('File does not exist')
