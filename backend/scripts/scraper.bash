#!/bin/bash

#title         :scraper.bash
#description   :This script scans a directory for JPEGs and saves their comment data to a CSV
#author        :Jay Goldberg
#date          :20150401
#license       :MIT
#version       :0.0.2
#usage         :bash scraper.bash <dir with day dirs> <filename.csv>
#notes         :make sure that column heading are stripped on each subsequent run of exiftool in the loop
#==============================================================================

for day in `ls ${1}`; do for hour in `ls ${1}/${day}`; do for file in `ls ${day}/${hour}`; do echo -n ${day}/${hour}/${file}, >> ${2}; rdjpgcom ${day}/${hour}/${file} | sed -n -e '2{p;q}' >> ${2}; done; done; done

# this method is actually slower! thought that one file write per loop would be faster...
#for day in `ls ${1}`; do for hour in `ls ${1}/${day}`; do for file in `ls ${day}/${hour}`; do filepath="${day}/${hour}/${file},"; comment=$(rdjpgcom ${day}/${hour}/${file} | sed -n -e '2{p;q}'); echo ${filepath}{$comment} >> ${2}; done; done; done
