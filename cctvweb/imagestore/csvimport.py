from django.db import models
from imagestore.models import Image
import os, sys
import csv
import json
import datetime

print("Started")

f = open(os.path.join('..', 'data', 'sanitized.csv'))
reader = csv.reader(f)

for row in reader:
    # parse the json field in the CSV
    decoded = json.loads(row[1])
    
    # this test does not add appreciably to the insert time
    if decoded['IQimage']['event'] == ['motion']:
        insert_motion_windows = decoded['IQimage']['motionWindows']
    else:
        insert_motion_windows = ''
    
    # datetime expects a decimal, not an extended UNIX time string, thus /1000.0
    # trigger_type & motion_windows are not ideal as they are stored as arraya == bad db normalization
    imageFrame = Image(path = row[0], raw_json = row[1], timestamp = datetime.datetime.utcfromtimestamp(decoded['IQimage']['time']/1000.0), imgjdbg = decoded['IQimage']['imgjdbg'],  sequence_number = decoded['IQimage']['sequence'], trigger_type = decoded['IQimage']['event'],  motion_windows = insert_motion_windows)
    
    imageFrame.save()

f.close()
