__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "Apache 2.0"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

class Config(object):
  """ list of cameras and where their images are stored 
      Must not have special chars
      Path is relative to the client (browser), use trailing slash 
      will likely be put in the MongoDB at some point
      the real paths are served by nginx and are defined as aliases there
      but the final dir must match what's on disk
      The functionality exists to have the name and path differ"""
      
  CAMERAS = {
    'pond': 'images/pond/',
    'birdnest': 'images/birdnest/',
    'frontdoor': 'images/frontdoor/'
  }

  # turn debugging on , will show flask errors
  DEBUG = True
  
  # time that must elapse before the next JPEG is consdered a new event
  DEFAULT_DWELL_SECS = 3
  
  # mongodb://<user>:<password>@<host>:<port>/>
  MONGO_URI = 'mongodb://localhost:27017/'
  MONGO_DB = 'mydb'
  
  # TODO: artificial result limit to prevent it from killing your server ;-)
  RESULT_LIMIT = 10000
  
  # used to estimate bandwidth requirred
  AVG_FILE_SIZE = 300
  
  # hostname of the backend API
  HOSTNAME = 'cctv.yourdomain.com'
  
  # CNAMEs used to distribute static image requests to overcome te limit on
  # concurrent connnections to a single hostname
  CNAMES = [
    'static1.yourdomain.com',
    'static2.yourdomain.com',
    'static3.yourdomain.com',
    'static4.yourdomain.com'
  ]
