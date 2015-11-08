#!/bin/bash

#title         :scraper.bash
#description   :This script scans a directory for JPEGs and saves their comment data to a CSV
#author        :Jay Goldberg
#url           :https://github.com/JayGoldberg/CCTVweb
#license       :Apache 2.0
#usage         :bash scraper.bash <dir with day dirs> <filename.csv>
#==============================================================================

path=$1
csvpath=$2
totalcount=0 # set this first or USR1 will kill the script if you send 
# the signal before the var has been assigned
currentcount=0

sigusr1()
{
   echo "${currentcount}/${totalcount}"
}

trap 'sigusr1' USR1

totalcount=$(find ${path} -type f -name *.jpg|wc -l)

for day in ${path}/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]
  do for hour in ${day}/??
    do for imagefilepath in ${hour}/*.jpg
      do
        json=''
        json=$(rdjpgcom ${imagefilepath}|sed -n '2p')
        # ensure atomicity, do not write half-lines! Use empty assignment as an indicator 
        if [ -n "$json" ]
          then
            echo ${imagefilepath},${json} >> ${csvpath}
          else
            echo "Bad file!"
        fi
        currentcount=$((currentcount + 1))
      done
    done
  done

