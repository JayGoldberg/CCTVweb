__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "MIT"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"
__status__ = "Alpha"

class Config(object):
  """ list of cameras and where their images are stored 
      Must not have special chars
      Path is relative to the client (browser), use trailing slash """
  CAMERAS = {
    'pond': 'http://127.0.0.1/images/pond/',
    'birdnest': 'http://127.0.0.1/images/birdnest/',
    'frontdoor': 'http://127.0.0.1/images/frontdoor/',
    'backalley': 'file:///mnt/smb/myserver/iqeye/backalley/' # (Linux) make sure you have your SMB share mounted there
  }

  DEFAULT_DWELL_SECS = 3
  # mongodb://<user>:<password>@<host>:<port>/>
  MONGO_URI = 'mongodb://localhost:27017/'
  MONGO_DB = 'mydb'
  RESULT_LIMIT = 10000
  DEBUG = True
  AVG_FILE_SIZE = 300
