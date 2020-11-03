#!/bin/bash

cellLength=2.415769
units=14

for (( i=1; i<=$units; i++ ))
do
	fileName=acene${i}.txt
	echo $i,$fileName
	cat unit_cell_PCrightEnd.txt > $fileName
	cat unit_cell_PC.txt >> $fileName
	cellLength=2.415769
	shifts=$cellLength
	for (( j=1; j<i; j++ ))
	do
                shifts=$(echo $cellLength*$j | bc)
                echo inside inner do $j, $shifts
		cat unit_cell_PC.txt | awk '{printf "%s   %.4f   %.8g   %.8g\n",$1,$2,$3,$4=$4+c}' c=$shifts >> $fileName

#		shifts=$(echo $cellLength*$j | bc)
#		echo inside inner do $j, $shifts
	done
	echo $shifts
	shifts=$(echo $cellLength*$i | bc)
	cat unit_cell_PC-end.txt | awk '{printf "%s   %.4f   %.8g   %.8g\n",$1,$2,$3,$4=$4+c}' c=$shifts >> $fileName
done
