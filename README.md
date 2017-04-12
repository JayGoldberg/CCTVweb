CCTVweb
=======
Browse and manage JPEG images written to FTP by IQinvision IQeye IP cameras, in a nice web-based app!

JPEGs are grouped together into events, and events can be replayed in real-time or by mouse movement. The player is a still-frame player based on open web technologies.

Architecture
============
CCTVweb currently depends on the JPEG comment (COM) fields written by IQinvision IQeye network cameras. Cameras are responsible for FTP'ing images, but no further intelligence is needed from them, the indexing, management, and playback is handled by CCTVweb.

Implemented Features
============
 - Completely web-based viewer, no plugins required
   * Play events forwards/backwards
 - Scroll through events frame-by-frame
 - Fast JPEG indexing
 - AngularJS frontend
 - Fast backend engine for returning image data
 - Nice graphs of camera activity
 - CORS support and static file serving

Planned Features
============
 - Preview all events for a single day
 - Play events sequentially
 - Support for live viewer and "popping" interesting cameras to foreground
 - Set alert thresholds
   - ie. if camera is recording over 25% more motion today than yesterday, send an email
 - Excellent support for small/cheap computers (CHiP, Raspberry Pi)
 - Support for Google Cloud Storage
 - Image recognition capability using Google Machine Vision
 - Support for relays (for door locks), HTTP triggers
 - Camera settings query and management

Requirements
============
 * Linux server
 * nginx/lighttpd
 * python2
   * virtualenv
   * flask
   * Flask-RESTful
* sqlite3
* nodejs

Installation
============
1. `git clone` the source
1. Install prereqs
1. Import sample data from .csv into DB
1. Config app and nginx/lighttpd
1. Copy static files to your webserver or CDN
6. Run the backend
7. Open the frontend in a browser

### Python2
1. Install Python2, virtualenv
2. Create virtualenv and activate it
    - `virtualenv -p /usr/bin/python2 ./new-environment`
    - `source ./new-environment/bin/activate`
3. Install the pip packages (the other dependencies will be automatically pulled)
    - `pip install -r requirements.txt`

### Camera FTP configuration
1. Update your cameras to the latest firmware [IQinvision](http://www.iqeye.com).
2. Under the Trigger tab, set up FTP to write images, recommended to save each camera to its own directory and limit per-directory contents to less than 10,000 JPEGs
    -  See docs/iqinvision.md
