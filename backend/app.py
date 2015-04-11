#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"
__status__ = "Alpha"

import time, re
from flask import Flask, jsonify, request, render_template
from flask.ext.pymongo import PyMongo, MongoClient
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.cors import CORS

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing
cors = CORS(app)

app.config['DEBUG'] = True

# TODO: abstract this into a config file
app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_COLLECTION'] = 'images'

# establish DB connection
client = MongoClient()
db = client.mydb # how do I call the app.config vars above as strings?
collection = db.images # how do I call the app.config vars above as strings?

# get API going
api = Api(app)
    
# many events of many images, event grouping comes later
class Events(Resource):
  def get(self, start_datetime, end_datetime):
    # exclude _id or the JSON serializer freaks out
    
    # filter only +00 events
    #regex = re.compile('.*trig\+00.jpg')
    #result = collection.find({ '$and': [ { "IQimage.time" : { '$gt': int(epoch_start), '$lt': int(epoch_end) } }, {'path': {'$regex': regex} } ] }, { '_id': 0, 'IQimage.imgjdbg': 0, 'IQimage.sequence': 0 } ).sort("IQimage.time")
    result = collection.find({ "IQimage.time" : { '$gte': start_datetime, '$lte': end_datetime } }, { '_id': 0, 'IQimage.imgjdbg': 0, 'IQimage.sequence': 0 } ).sort("IQimage.time")
    
    return { 'args': request.args, 'result': list(result[0:200]), 'est_size': '%sMB' % round(((result.count() * 300)/1024),2), 'start_date': start_datetime, 'end_date': end_datetime, 'resultcount': result.count() }, 200

  def post(self, start_datetime, end_datetime):
    parser = reqparse.RequestParser()
    parser.add_argument('group', type=bool, help='group the events requires true or false', location='json', default=True)
    parser.add_argument('dwell_time_secs', type=int, help='time before the next activity is considered a new event', location='json', default=3)
    parser.add_argument('sloppy_results', type=bool, help='if the time window "cuts off" the event, those extra JPG frames are included anyway', location='json', default=False)
    
    args = parser.parse_args()
    print(args)
    
    result = collection.find({ "IQimage.time" : { '$gte': start_datetime, '$lte': end_datetime } }, { '_id': 0, 'IQimage.imgjdbg': 0, 'IQimage.sequence': 0 } ).sort("IQimage.time")

    if args['group'] == True and result.count() != 0:
      event_list = []
      results = list(result[0:10000]) # can only use this once, it empties the result object, REMOVE this limit after testing
      dwell_time = int(args['dwell_time_secs']) * 1000

      startFrame = results[0]['IQimage']['time']
      lastFrame = results[0]['IQimage']['time']
      
      frameCount = 0
      for image in results:
        frameCount += 1
        difference = image['IQimage']['time'] - lastFrame
        
        if difference > dwell_time:
          # this is a new event
          event_list.append([startFrame, lastFrame, frameCount])
          startFrame = image['IQimage']['time']
          frameCount = 0
        
        lastFrame = image['IQimage']['time']
        # BUG: last if there is no end to the last event, those JPGs are not included in the grouping
    
      return { 'args': request.args, 'result': event_list, 'resultcount': len(event_list) }, 200
    else:
      return { 'args': request.args, 'result': list(result[0:4000]), 'est_size': '%sMB' % round(((result.count() * 300)/1024),2), 'start_date': start_datetime, 'end_date': end_datetime, 'resultcount': result.count() }, 200
    
  def delete(self):
    return {'request data': request.args}

api.add_resource(Events, '/events/range/<int:start_datetime>/<int:end_datetime>/')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
