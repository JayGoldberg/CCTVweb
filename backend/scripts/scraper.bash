#!/bin/bash

#title         :scraper.bash
#description   :This script scans a directory for JPEGs and saves their comment data to a CSV
#author        :Jay Goldberg
#url           :https://github.com/JayGoldberg/CCTVweb
#license       :MIT
#usage         :bash scraper.bash <dir with day dirs> <filename.csv>
#==============================================================================

path=$1
totalcount=0 # set this first or USR1 will kill the script
currentcount=0

sigusr1()
{
   echo "${currentcount}/${totalcount}"
}

trap 'sigusr1' USR1

totalcount=$(find ${path} -type f -name *.jpg|wc -l)

for day in ${path}/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]
  do for hour in ${day}/??
    do for imagefile in ${hour}/*.jpg
      do
        # ensure atomicity, do not write half-lines! Use assignment failure as an indicator 
        json=$(rdjpgcom ${imagefile}|sed -n '2p')
        if [ $? -eq 0 ]
          then
            echo ${imagefile},${json} >> ${2}
        fi
        currentcount=$((currentcount + 1))
      done
    done
  done

