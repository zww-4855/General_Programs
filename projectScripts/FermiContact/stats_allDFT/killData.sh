#!/bin/bash

while read line
do
	echo $line
	outfile=$( echo correct_$line )
	sed  106d $line | sed  105d | sed 103d | sed 102d | sed 98d | sed 97d | sed 96d | sed 88d | sed 87d | sed 83d | sed 82d | sed 77d | sed 72d | sed 68d | sed 67d | sed 62d | sed 59d | sed 55d | sed 54d | sed 51d | sed 49d | sed 39d | sed 34d | sed 33d | sed 30d | sed 27d | sed 23d | sed 17d >> $outfile


done < infiles.txt
