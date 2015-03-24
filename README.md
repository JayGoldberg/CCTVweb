CCTVweb
=======
Browse and manage MJPEG (motion JPEG) images written to FTP from IQinvision IQeye IP Cameras through a web interface

Events are grouped together and individual events can be replayed in real-time or by mouse wheel scrolling. The player is based on JavaScript CSS.

Architecture
============
CCTVweb currently depends on the JPEG comment (COM) fields written by IQinvision IQeye network cameras. Using a perl script, this data is read, and is inserted into a database. A web frontend interfaces with a Python Flask backend to offer a browser-based event viewer, an interface to run queries and set warnings and limits on cameras. Cameras are responsible for FTP'ing images, but no further intelligence is needed from them.

Planned Features
============
* Completely web-based viewer
* Preview all events for a single day
* Play events sequentially
* Play events forwards backwards
* Scroll through events frame-by-frame
* Set alert thresholds
  * ie. if camera is recording over 25% more motion today than yesterday, send an email
* Fast backend engine for returning image data
* AngularJS frontend

Requirements
============
* Linux server
* perl
  * exiftool
* python3
  * virtualenv
  * flask
  * Flask-PyMongo
  * Flask-RESTful
  * Flash-CORS
* mongodb

Installation
============
1. Get the most recent source:
  - git clone https://github.com/JayGoldberg/CCTVweb
2. Install mongodb
3. Install Python3 and pre-reqs below
4. Import sample data from .csv into mongodb
`CCTVweb/backend/scripts/csvimport.py CCTVweb/data/sanitized.csv`
5. Generate indexes on IQimage.time field in mongo
`db.images.createIndex( { "IQimage.time": 1 } )`
6. Run the backend
`CCTVweb/backend/app.py`
7. Open the frontend in a browser
`CCTVweb/frontend/index.py`

### Python3
1. Install Python3, virtualenv
2. Create virtualenv and activate it
  - virtualenv -p /usr/bin/python3 ./new-environment
  - source ./new-environment/bin/activate
3. Install the pip packages (the other dependencies will be automatically pulled)
  - pip install flask flask-pymongo flask-restful flask-cors

### Camera FTP configuration
1. Update your cameras to the latest firmware [IQinvision](http://www.iqeye.com).
2. Under the Trigger tab, set up FTP to write images to filename "$ST.$FN", and directory "$SH/$SD(%Y)-$SD(%m)-$SD(%d)/$SD(%H)"
  -  See docs/iqinvision.md

This will create file paths like "camera/00_34_33:e3:b4:81/2016-01-01/23/23_01.trig+00.jpg. It is important that this schema matches what is defined in config/config.py. Make sure that you define this schema in such a way as to not write an excessive number of files to a single directory as this will negatively impact performance.
