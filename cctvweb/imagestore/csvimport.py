from django.db import models
from imagestore.models import Image
import os, sys
import csv
import json
import datetime

print("Started")

f = open('../data/sanitized.csv')
reader = csv.reader(f)

for row in reader:
    # parse the json
    decoded = json.loads(row[1])
    
    # datetime expects a decimal, not an extended UNIX time string, thus /1000.0
    # trigger_type below is not ideal as it will store an array == bad db normalization
    imageFrame = Image(path = row[0], raw_json = row[1], timestamp = datetime.datetime.utcfromtimestamp(decoded['IQimage']['time']/1000.0), imgjdbg = decoded['IQimage']['imgjdbg'], sequence_number = decoded['IQimage']['sequence'], trigger_type = decoded['IQimage']['event'])
    
    imageFrame.save()

f.close()
