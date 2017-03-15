## Scripts

Here we have some helper scripts for gathering data from JPEGs and getting that data into MongoDB.

### iqeye_jpeg_scraper.py

Traverse a directory structure, find all JPEGs and scrape their comment data into a CSV.

### sqlite_import.py

Takes a csv file with the following schema:

`path,{ json: "data" }`

and inserts each as a record in a SQLite DB.
