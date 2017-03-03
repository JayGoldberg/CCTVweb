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
import sqlite3

def recordgenerator(filepath):

  print('Opening file %s' % filepath)

  # TODO: put this in a try block
  with open(filepath, 'r') as f:
    for lineno, content in enumerate(f):
      pass
  
    f.seek(0)
    
    mylist = []
    for line in f:
      pair = line.split(',', 1)
      path = pair[0] # the first element is always the path
      decoded = json.loads(pair[1]) # parse the json field in the CSV
      #mylist += [path, decoded['IQimage']['time']]
      yield (path, decoded['IQimage']['time'],)

if __name__ == '__main__':
  dbname = sys.argv[1]
  camname = sys.argv[2]
  filepath = sys.argv[3]
  
  # example JSON: {"IQimage":{"sequence":2542282,"time":1408160269221,"event":["none"],"imgjdbg":" 998/004:16/5/167:080/071/01/4/57/70/20/00:06/06/09:c3"}}

  table_name=camname
  field1='path'
  field2='rawjson'
  field3='time'
  field4='event'
  field5='isDeleted'
  field1_type='TEXT'
  field2_type='TEXT'
  field3_type='INTEGER'
  field4_type='TEXT'
  field5_type='INTEGER'
  
  conn = sqlite3.connect(dbname)
  
  c = conn.cursor()
  
  c.execute('CREATE TABLE IF NOT EXISTS {}({} {}, {} {}, {} {}, {} {})'\
  .format(table_name, field1, field1_type, field2, field2_type, field3, field3_type, field4, field4_type, field5, field5_type))

  c.executemany('INSERT INTO {}(path, time) VALUES(?, ?)'.format(table_name), recordgenerator(filepath))

  c.execute('CREATE INDEX times ON apt(time)')
  conn.commit()
  conn.close()
