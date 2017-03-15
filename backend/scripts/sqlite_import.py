#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "Apache 2.0"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

import os
import sys
import json
import sqlite3

def recordgenerator(camname, filepath):

  print('Opening file %s' % filepath)

  # TODO: put this in a try block
  with open(filepath, 'r') as f:
    for lineno, content in enumerate(f):
      pass
  
    f.seek(0)

    for line in f:
      # TODO: reintroduce status functionality (progress)
      #print("{0:.0f}%".format((float(i) / lineno) * 100))
      # TODO: use csv library instead of naive split
      pair = line.split(',', 1)
      path = pair[0] # the first element is always the path
      # TODO: error handling for when JSON is not JSON
      decoded = json.loads(pair[1]) # parse the json field in the CSV
      yield (camname, path, pair[1], decoded['IQimage']['time'], json.dumps(decoded['IQimage']['event']), False)

if __name__ == '__main__':
  dbname = sys.argv[1]
  camname = sys.argv[2]
  filepath = sys.argv[3]
  
  # example JSON: {"IQimage":{"sequence":2542282,"time":1408160269221,"event":["none"],"imgjdbg":" 998/004:16/5/167:080/071/01/4/57/70/20/00:06/06/09:c3"}}

  schema = [
      #'cam_id INT',
      'cam_name TEXT',
      'path TEXT',
      'rawjson TEXT',
      'time INTEGER',
      'event TEXT',
      'isDeleted INTEGER',
      #'FOREIGN KEY() REFERENCES cameras(id)',
  ]

  conn = sqlite3.connect(dbname)
  
  c = conn.cursor()

  schemastring = ''.join(['{}, '.format(field) for field in schema])[:-2]
  
  c.execute('CREATE TABLE IF NOT EXISTS {}({})'\
      .format('images', schemastring))

  # needed when /tmp is too small
  # choose a directory that has enough space for the csv in question
  # TODO: detect available space compared to input file, have a runtime flag
  c.execute('PRAGMA temp_store = 1')
  c.execute('PRAGMA temp_store_directory = "/tmp"')

  c.executemany('INSERT INTO {}(cam_name, path, rawjson, time, event, isDeleted) VALUES(?, ?, ?, ?, ?, ?)'\
      .format('images'), recordgenerator(camname, filepath))

  c.execute('CREATE INDEX IF NOT EXISTS times ON {}(time)'.format('images'))
  conn.commit()
  conn.close()
