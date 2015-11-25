##Scripts

Here we have some helper scripts for gathering data from JPEGs and getting that data into MongoDB.

##mongochunkimport.py

This module addresses a problem in which if you try to load an entire set of json data into MongoDB in one chunk, either Mongo or Python will eat all of the memory and be killed. Intead, this breaks up the submission into nice chunks, saving memory.

##csvimport.py

Takes a csv file with the following schema:

`path,{ json: "data" }`

and puts each line as a Mongo document

##scraper.bash

Reads a bunch of JPEGs using rdjpgcom and keeps appending to a textfile which can then be used with csvimport.py to populate the MongoDB.
