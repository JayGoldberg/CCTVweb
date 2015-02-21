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
from flask.ext.restful import Api, Resource
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

# single event of many images, image grouping comes later
class Event(Resource):
  def get(self, event_id):
    return {'request data': request.args, 'event_id': event_id}

  def post(self):
    return {'request data': request.args}
    
  def delete(self):
    return {'request data': request.args}
    
# many events of many images, event grouping comes later
class Events(Resource):
  def get(self, start_date, end_date):
    pattern = '%Y-%m-%d'
    epoch_start = int(time.mktime(time.strptime(start_date, pattern)))*1000
    epoch_end = int(time.mktime(time.strptime(end_date, pattern)))*1000
    # exclude _id or the JSON serializer freaks out
    
    # filter only +00 events
    #regex = re.compile('.*trig\+00.jpg')
    #result = collection.find({ '$and': [ { "IQimage.time" : { '$gt': int(epoch_start), '$lt': int(epoch_end) } }, {'path': {'$regex': regex} } ] }, { '_id': 0, 'IQimage.imgjdbg': 0, 'IQimage.sequence': 0 } ).sort("IQimage.time")
    result = collection.find({ "IQimage.time" : { '$gt': int(epoch_start), '$lt': int(epoch_end) } }, { '_id': 0, 'IQimage.imgjdbg': 0, 'IQimage.sequence': 0 } ).sort("IQimage.time")
    return {'request data': request.args, 'est_size': '%sMB' % round(((result.count() * 300)/1024),2), 'start_date': epoch_start, 'end_date': epoch_end, 'results': list(result), 'resultcount': result.count()}, 200

  def post(self):
    return {'request data': request.args}
    
  def delete(self):
    return {'request data': request.args}

api.add_resource(Events, '/events/range/<string:start_date>/<string:end_date>/')

if __name__ == '__main__':
    app.run()
