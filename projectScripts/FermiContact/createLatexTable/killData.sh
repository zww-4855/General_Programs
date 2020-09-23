#!/bin/bash
# PURPOSE:: KILLS EMPTY LINES SEPARATING MOLECULES
# use on DFT data only
# ie infiles.txt consists of DFT datafiles containg FC info

while read line
do

#sed 104d $line | sed 99d | sed 88d | sed 87d | sed 83d | sed 82d | sed 77d | sed 72d | sed 68d | sed 67d | sed 62d | sed 59d | sed 39d | sed 35d | sed 27d | sed 17d >> copy_$line 
sed 86d $line | sed 81d | sed 75d | sed 72d | sed 69d | sed 65d | sed 61d | sed 58d | sed 55d | sed 52d | sed 48d | sed 44d | sed 40d | sed 36d | sed 33d | sed 30d | sed 26d | sed 23d | sed 20d | sed 17d | sed 15d | sed 12d | sed 9d | sed 6d | sed 3d > KLcopy_$line
done < infiles.txt


#separate DFT data into 2 columns for table
while read line
do
	sed -n 1,33p KLcopy_$line | awk '{print $2}' > KLcopyA_$line
	sed -n 34,65p KLcopy_$line | awk '{print $2}' > KLcopyB_$line
done < infiles.txt



