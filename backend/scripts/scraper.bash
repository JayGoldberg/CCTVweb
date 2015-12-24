#!/bin/bash

#title         :scraper.bash
#description   :This script scans a directory for JPEGs and saves their comment data to a CSV
#author        :Jay Goldberg
#url           :https://github.com/JayGoldberg/CCTVweb
#license       :Apache 2.0
#usage         :bash scraper.bash <dir with day dirs> <filename.csv>
#==============================================================================

path=$1
totalcount=0 # set this first or USR1 will kill the script if you send 
# the signal before the var has been assigned
currentcount=0

sigusr1()
{
  echo "${currentcount}/${totalcount}"
}

trap 'sigusr1' USR1

# if path not defined
echo "Path not specified on commandline, using working path" >&2
if [ -z "$path" ]; then
  path=$(pwd)

totalcount=$(find ${path} -type f -name '*.jpg'|wc -l)

read_com() {
  json=''
  json=$(rdjpgcom "$1"|sed -n '2p')
  # ensure atomicity, do not write half-lines! Use empty assignment as an indicator 
  if [ -n "$json" ]; then
    echo ${1},${json}
  else
    echo "Bad file!" >&2
}

while read path; do
  #echo $path
  read_com "$path"
  currentcount=$((currentcount + 1))
done < <(find ${path} -type f -name '*.jpg')
