from django.db import models
from imagestore.models import Image
import os, sys
import csv
import json
from pprint import pprint
import datetime

print("Started")

f = open('../data/sanitized.csv')
reader = csv.reader(f)

for row in reader:
    # parse the json
    decoded = json.loads(row[1])
    
    #pprint(decoded)
    
    #if decoded['IQimage']['event'][0] == 'motion':
    #    print(decoded['IQimage']['motionWindows'])
    print(decoded['IQimage']['time'])
   
    imageFrame = Image()
    imageFrame.path = row[0]
    imageFrame.raw_json = row[1]
    #imageFrame.mac = 
    # datetime expects a decimal, not an extended UNIX time string
    imageFrame.timestamp = datetime.datetime.utcfromtimestamp(decoded['IQimage']['time']/1000.0)
    imageFrame.imgjdbg = decoded['IQimage']['imgjdbg']
    imageFrame.sequence_number = decoded['IQimage']['sequence']
    imageFrame.trigger_type = decoded['IQimage']['event'] # this is not ideal as it will store an array
    imageFrame.save()

f.close()
