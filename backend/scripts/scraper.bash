#!/bin/bash

#title         :scraper.bash
#description   :This script scans a directory for JPEGs and saves their comment data to a CSV
#author        :Jay Goldberg
#url           :https://github.com/JayGoldberg/CCTVweb
#license       :MIT
#usage         :bash scraper.bash <dir with day dirs> <filename.csv>
#==============================================================================

for day in ${1}/*
  do for hour in ${day}/*
    do for path in ${hour}/*.jpg
      do 
        if [ -f ${path} ]
          then
            comment=$(rdjpgcom ${path})
            if [ $? -eq 0 ]
              then
                json=$(cut -d' ' -f2 <<< ${comment})
                echo ${path},${json} >> ${2}
            fi

        fi
      done
    done
  done

# this method is actually slower! thought that one file write per loop would be faster...
#for day in  ${1}/*
#  do for hour in ${day}/*
#    do for file in ${hour}/*
#      do
#        filepath=${file},"; comment=$(rdjpgcom ${file} | sed -n -e '2{p;q}'); echo ${filepath}{$comment} >> ${2}
#      done
#    done
# done
