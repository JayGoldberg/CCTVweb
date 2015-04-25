#!/bin/bash

#title         :scraper.bash
#description   :This script scans a directory for JPEGs and saves their comment data to a CSV
#author        :Jay Goldberg
#license       :MIT
#usage         :bash scraper.bash <dir with day dirs> <filename.csv>
#notes         :make sure that column heading are stripped on each subsequent run of exiftool in the loop
#==============================================================================

for day in ${1}/*
    do for hour in ${day}/*
        do for file in ${hour}/*.jpg
        do if [ -f ${file} ]
        then
            echo -n ${file}, >> ${2}
            rdjpgcom ${file} | sed -n -e '2{p;q}' >> ${2}
        fi
        done
    done
done

# this method is actually slower! thought that one file write per loop would be faster...
#for day in  ${1}/*; do for hour in ${day}/*; do for file in ${hour}/*; do filepath=${file},"; comment=$(rdjpgcom ${file} | sed -n -e '2{p;q}'); echo ${filepath}{$comment} >> ${2}; done; done; done
