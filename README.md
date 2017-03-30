CCTVweb
=======
Browse and manage JPEG images written to FTP by IQinvision IQeye IP cameras, in a nice web-based app!

JPEGs are grouped together into events, and events can be replayed in real-time or by mouse movement. The player is a still-frame player based on open web technologies.

Architecture
============
CCTVweb currently depends on the JPEG comment (COM) fields written by IQinvision IQeye network cameras. Cameras are responsible for FTP'ing images, but no further intelligence is needed from them, the indexing, management, and playback is handled by CCTVweb.

Planned Features
============
* Completely web-based viewer, no plugins required
* Preview all events for a single day
* Play events sequentially
* Play events forwards/backwards
* Scroll through events frame-by-frame
* Support for live streaming and "popping" interesting cameras to foreground
* Set alert thresholds
  * ie. if camera is recording over 25% more motion today than yesterday, send an email
* Fast JPEG indexing
* Fast backend engine for returning image data
* Excellent support for small/cheap computers (CHiP, Raspberry Pi)
* AngularJS frontend
* Support for Google Cloud Storage
* Nice graphs of camera activity
* Image recognition capability using Google Machine Vision
* CORS support and static file serving
* Support for relays (for door locks), HTTP triggers

Requirements
============
* Linux server
* nginx/lighttpd
* python3
  * virtualenv
  * flask
  * Flask-RESTful
* sqlite3
* nodejs

Installation
============
1. `git clone` the source
1. Install pre-reqs
1. Import sample data from .csv into mongodb
1. Config app and nginx/lighttpd
1. Copy static files to your webserver or CDN
6. Run the backend
7. Open the frontend in a browser

### Python3
1. Install Python3, virtualenv
2. Create virtualenv and activate it
    - virtualenv -p /usr/bin/python3 ./new-environment
    - source ./new-environment/bin/activate
3. Install the pip packages (the other dependencies will be automatically pulled)
    - pip install flask flask-pymongo flask-restful flask-cors

### Camera FTP configuration
1. Update your cameras to the latest firmware [IQinvision](http://www.iqeye.com).
2. Under the Trigger tab, set up FTP to write images, recommended to save each camera to its own directory and limit per-directory contents to less than 10,000 JPEGs
    -  See docs/iqinvision.md
