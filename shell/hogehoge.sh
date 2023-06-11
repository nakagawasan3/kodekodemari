#!/bin/bash

while read row; do
  column1=`echo ${row} | cut -d , -f 1`
  column2=`echo ${row} | cut -d , -f 2`
  column3=`echo ${row} | cut -d , -f 3`
  
  html=`curl -s ${column3}`
  title=`echo ${html} | grep -o '<title.*</title>' | sed 's/<title[^>]*>\(.*\)<\/title>/\1/g'`
  
  intId=`echo "${column2}" |  sed -e 's/[^0-9]//g'`
  unixTime=$((intId / 2**22 + 1288834974657))
  tweetDate=$(date -d @$((unixTime/1000-(9*60*60))) '+%Y%m%d%H%M%S')
  
  echo "${column3},${tweetDate},${title}" >> hogehoge_02.csv
  
  sleep 10
done < hogehoge_01.csv
