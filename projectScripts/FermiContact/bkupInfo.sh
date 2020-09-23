#!/bin/bash
#Program Goal: Backup ZMAT and output file from various calculations 
for dir in */; do   # *.inp; do
  cd $dir
  echo $dir
  pwd
  mkdir ../smallMoleculeOptBkup/$dir
  cp ZMAT ../smallMoleculeOptBkup/$dir
  cp *.out ../smallMoleculeOptBkup/$dir

  echo
  cd ../
done
