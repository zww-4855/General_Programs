#!/bin/bash

while read p; do
        echo $p
        echo ${p}.txt
        mkdir $p
        cd $p
        cp ../${p}.txt .
        cp ../example.py .

	fileName=${p}.txt

	sed "32r ${fileName}" example.py > submit.py
#        sed -n '/^*/,/^*/p' *.inp > temp.txt
#        sh ../modify.sh
        cd ..
done < readlist.txt 
