#/bin/bash
# FOR RSH FC FROM ORCA USE ONLY!!!


for dir in */; do
	cd $dir
	rm FC_*
	# For atom labeling - determines number of A(iso) values to harvest
lineNum=$(wc -l *.xyz | awk '{print $1}')
echo $dir
lineNum=$((lineNum-2)) # offsets 2 lines as a result of ORCA optimization
grep -m $lineNum "Nucleus" *FC.out | awk '{print $2}' > atomLabeling.txt
diffNum=$lineNum  #$((lineNum+1))
 count=0


grep "A(iso)=" *FC.out | sed 's/^.*= //' > FCresults.txt

### TO DO::
### Depending on the assortment of DFT jobs run under one ORCA input file
### this section will change. So this is an example I have 1 input file that runs 
### a Fermi Contact calculation using the qtp00,qtp01,qtp02,camb3lyp,wb97x,lcblyp 
### functionals
 while read line; do  
	 if [[ $(($count / $diffNum )) -eq 0 ]]; then
		 echo $line >> FC_qtp00.txt
         elif [[ $(($count / $diffNum )) -eq 1 ]]; then
                 echo $line >> FC_qtp01.txt
         elif [[ $(($count / $diffNum )) -eq 2 ]]; then
                 echo $line >> FC_qtp02.txt
         elif [[ $(($count / $diffNum )) -eq 3 ]]; then
                 echo $line >> FC_camb3lyp.txt
         elif [[ $(($count / $diffNum )) -eq 4 ]]; then
                 echo $line >> FC_wb97x.txt
         elif [[ $(($count / $diffNum )) -eq 5 ]]; then
                 echo $line >> FC_lcblyp.txt
	 fi
         count=$((count+1))

 done < FCresults.txt
paste atomLabeling.txt FC_qtp00.txt > FC_qtp00FINAL.txt
paste atomLabeling.txt FC_qtp01.txt > FC_qtp01FINAL.txt
paste atomLabeling.txt FC_qtp02.txt > FC_qtp02FINAL.txt
paste atomLabeling.txt FC_camb3lyp.txt > FC_camb3lypFINAL.txt
paste atomLabeling.txt FC_wb97x.txt > FC_wb97xFINAL.txt
paste atomLabeling.txt FC_lcblyp.txt > FC_lcblypFINAL.txt

cd ../
done
