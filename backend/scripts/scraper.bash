#!/bin/bash

#title           :scraper.bash
#description     :This script scans a directory for JPEGS and saves their comment data to a CSV
#author		 :Jay Goldberg
#date            :20141101
#version         :0.1
#usage		 :bash scraper.bash <dir with hour dirs> <filename.csv>
#notes           :make sure that column heading are stripped on each subsequent run of exiftool in the loop
#==============================================================================

for hour in "$1"/??; do exiftool -r -a -G4 -csv -Comment "$hour" >> $2; done
