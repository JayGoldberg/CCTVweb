#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2017"
__credits__ = ["Jay Goldberg"]
__license__ = "Apache 2.0"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

import os
import sys
import json
import sqlite3

def recordgenerator(csvfilepath):

  print('Opening file %s' % csvfilepath)

  # TODO: put this in a try block
  with open(csvfilepath, 'r') as f:
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
      yield (path, pair[1], decoded['IQimage']['time'], json.dumps(decoded['IQimage']['event']))

if __name__ == '__main__':
  dbname = sys.argv[1] # path to .sqlite file, should be camera name
  csvfilepath = sys.argv[2] # path to csv file with 2 fields, no header
  
  # example JSON: {"IQimage":{"sequence":2542282,"time":1408160269221,"event":["none"],"imgjdbg":" 998/004:16/5/167:080/071/01/4/57/70/20/00:06/06/09:c3"}}

  schema = [
      #'cam_id INT',
      'path TEXT',
      'rawjson TEXT',
      'time INTEGER',
      'event TEXT',
      #'mac_addr' TEXT,
      #'FOREIGN KEY() REFERENCES cameras(id)',
  ]

  conn = sqlite3.connect(dbname)
  
  c = conn.cursor()
  schemastring = ''.join(['{}, '.format(field) for field in schema])[:-2]
  
  c.execute('CREATE TABLE IF NOT EXISTS {}({})'.format('images', schemastring))

  # needed when /tmp is too small
  # choose a directory that has enough space for the csv in question
  # TODO: detect available space compared to input file, have a runtime flag
  c.execute('PRAGMA temp_store = 1')
  c.execute('PRAGMA temp_store_directory = "/tmp"')

  c.executemany('INSERT INTO {}(path, rawjson, time, event) \
      VALUES(?, ?, ?, ?)'.format('images'), recordgenerator(csvfilepath))

  c.execute('CREATE INDEX IF NOT EXISTS times ON {}(time)'.format('images'))
  c.execute('CREATE TABLE IF NOT EXISTS {}({})'\
      .format('image_delete', 'path'))
  c.execute('CREATE TRIGGER aft_delete AFTER DELETE ON {} BEGIN INSERT into \
      {}(path) VALUES (OLD.path); END'.format('images', 'image_delete'))
  conn.commit()
  conn.close()
