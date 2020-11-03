#!/bin/bash

while read p; do
        echo $p
        echo ${p}.txt
        mkdir $p
        cd $p
        cp ../${p}.out .
        cp ../example.py .

	fileName=${p}.out

	sed "32r ${fileName}" example.py > submit.py
#        sed -n '/^*/,/^*/p' *.inp > temp.txt
#        sh ../modify.sh
        cd ..
done < readlist.txt 
