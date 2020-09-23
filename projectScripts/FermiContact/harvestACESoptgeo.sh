#!/bin/bash
## Program Goal: Harvest the optimized geometries from ACESII output file for later use in ORCA input file 
for dir in */; do 
  cd $dir
  echo $dir
  pwd
  IFS=/ read var1 var2 <<< $dir
  echo "var 1 is:"
  echo "$var1"
  var3="${var1}.xyz"

  sed -n '/optimized Cartesian/,/Hessian at convergence/p' *.out | tail -n +3 | head -n -2  > aces_coords.txt
  sed -n 1,2p $var3 > orcaheader.txt 
  cat aces_coords.txt >> orcaheader.txt
  
  cp *.xyz BKUPxyz.txt
  mv orcaheader.txt $var3

  cd ../
done
