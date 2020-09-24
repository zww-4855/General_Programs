#!/bin/bash

count=1
rm PBED3coords.txt
echo "********************************************************************************************" > PBED3coords.txt 
echo "********************************************************************************************" >> PBED3coords.txt
echo "****************************  DFT XC functional: PBED3      *********************************" >> PBED3coords.txt
echo "****************************  Basis: 6-31G**                *********************************" >> PBED3coords.txt
echo "****************************  Optimization Criteria: Tight  **********************************" >> PBED3coords.txt
echo >> PBED3coords.txt

while read -r line; do
if [ -d $line ]
then

cd $line
pwd
FILE1=$line.log
FILE3=*.log
FILE2=$line.out
FILE4=*.out

struct=$(sed -n ${count}p ../pbed3_label.txt )

if [ -f "$FILE1" ]; then

# find electronic energy
string1=$(grep "\HF=.*" $FILE1 | tail -n 1)
string2=$(grep "\RMSD=.*" $FILE1)
echo $string1$string2
IFS=
echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1

var=$(echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1)
IFS="="
energy=$(echo $var | awk '{print $2}')
#print geometry
echo "****************************  Structure ($count) : $struct            **************************" > ${line}OptCoords.txt
echo "****************************  Energy (au): $energy            **************************" >> ${line}OptCoords.txt
grep -A 22 "                         Standard orientation:" ${line}.log | tail -n 22 >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt

cat ${line}OptCoords.txt >> ../PBED3coords.txt


elif [ -f *.log ]; then

# find electronic energy
string1=$(grep "\HF=.*" *.log | tail -n 1)
string2=$(grep "\RMSD=.*" *.log )
echo $string1$string2
IFS=
echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1

var=$(echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1)
IFS="="
energy=$(echo $var | awk '{print $2}')

#print geometry
echo "****************************  Structure ($count) : $struct            **************************" > ${line}OptCoords.txt
echo "****************************  Energy (au): $energy            **************************" >> ${line}OptCoords.txt
grep -A 22 "                         Standard orientation:" ${FILE3} | tail -n 22 >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt

cat ${line}OptCoords.txt >> ../PBED3coords.txt

elif [ -f *.out ]; then

# find electronic energy
string1=$(grep "\HF=.*" *.out | tail -n 1)
string2=$(grep "\RMSD=.*" *.out )
echo $string1$string2
IFS=
echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1

var=$(echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1)
IFS="="
energy=$(echo $var | awk '{print $2}')

#print geometry
echo "****************************  Structure ($count) : $struct            **************************" > ${line}OptCoords.txt
echo "****************************  Energy (au): $energy            **************************" >> ${line}OptCoords.txt
grep -A 22 "                         Standard orientation:" ${FILE4} | tail -n 22 >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt

cat ${line}OptCoords.txt >> ../PBED3coords.txt


elif [ -f "$FILE2" ]; then

# find electronic energy
string1=$(grep "\HF=.*" $FILE2 | tail -n 1)
string2=$(grep "\RMSD=.*" $FILE2)
echo $string1$string2
IFS=
echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1

var=$(echo $string1$string2 | sed -n 's/.*\(HF=\)/\1/p' | cut -d "\\" -f 1)
IFS="="
energy=$(echo $var | awk '{print $2}')

#print geometry
echo "****************************  Structure ($count) : $struct            **************************" > ${line}OptCoords.txt
echo "****************************  Energy (au): $energy            **************************" >> ${line}OptCoords.txt
grep -A 22 "                         Standard orientation:" ${line}.out | tail -n 22 >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt

cat ${line}OptCoords.txt >> ../PBED3coords.txt

else
	echo
	echo no log files in
	echo Missing structure is: is $count
       	pwd 
	echo
echo "****************************  Structure ($count) : $struct            **************************" > ${line}OptCoords.txt
echo "****************************  Energy (au):             **************************" >> ${line}OptCoords.txt


echo >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt
echo >> ${line}OptCoords.txt

cat ${line}OptCoords.txt >> ../PBED3coords.txt

fi
count=$(( count + 1 ))
cd ..
else
	echo
	echo
	echo $line DOES NOT EXIST
	pwd
	echo
	echo
fi
done < pbed3Optinfiles.txt 



