#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "MIT"
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

# shared functions
def query(epoch_start, epoch_end):
  # exclude _id or the JSON serializer freaks out

  # filter only +00 events
  #regex = re.compile('.*trig\+00.jpg')
  #result = collection.find({ '$and': [ { "IQimage.time" : { '$gt': int(epoch_start), '$lt': int(epoch_end) } }, {'path': {'$regex': regex} } ] }, { '_id': 0, 'IQimage.imgjdbg': 0, 'IQimage.sequence': 0 } ).sort("IQimage.time")
  return collection.find({ "IQimage.time" : { '$gte': epoch_start, '$lte': epoch_end } }, { '_id': 0, 'IQimage.imgjdbg': 0, 'IQimage.sequence': 0 } ).sort("IQimage.time")

class Events(Resource):
    
  def get(self, start_datetime, end_datetime):
    result = query(start_datetime, end_datetime)
    
    return { 'args': request.args, 'result': list(result[0:200]), 'est_size': '%sMB' % round(((result.count() * 300)/1024),2), 'start_date': start_datetime, 'end_date': end_datetime, 'resultcount': result.count() }, 200

  def post(self, start_datetime, end_datetime):
    parser = reqparse.RequestParser()
    parser.add_argument('group', type=bool, help='group the events requires true or false', location='json', default=True)
    parser.add_argument('dwell_time_secs', type=int, help='time before the next activity is considered a new event', location='json', default=3)
    parser.add_argument('sloppy_results', type=bool, help='if the time window "cuts off" the event, those extra JPG frames are included anyway', location='json', default=False)
    
    args = parser.parse_args()
    print(args)
    
    result = query(start_datetime, end_datetime)

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
    
      return { 'args': request.args, 'result': event_list, 'resultcount': len(event_list) }, 200
    else:
      return { 'args': request.args, 'result': list(result[0:4000]), 'est_size': '%sMB' % round(((result.count() * 300)/1024),2), 'start_date': start_datetime, 'end_date': end_datetime, 'resultcount': result.count() }, 200
    
  def delete(self, start_datetime, end_datetime):
    #result = query(start_datetime, end_datetime)
    #for item in cursor:
      # broken until we find out how to allow _id to be passed without breaking the other HTTP methods, as we need _id to be able to update records
      #item.update( { "_id" :ObjectId("objectid_here") },{ $set : { "isDeleted":True } } )
    return {'request data': request.args}

# TODO: Multiple cameras, ie '/events/camid/<int:start_datetime>/<int:end_datetime>/
api.add_resource(Events, '/events/range/<int:start_datetime>/<int:end_datetime>/')
#api.add_resource(Reports, '/reports/<int:start_datetime>/<int:end_datetime>/') # FUTURE: daily, weekly, monthly reports. number of images, number of events, most active motion windows, daily size. Maybe this can be a component of the 'events' endpoint instead

if __name__ == '__main__':
  app.run(host="0.0.0.0")
