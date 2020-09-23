#!/bin/bash
### Organizes all fermi contact information for all molecules in the subdirectory tree into one file
rm final_camb3lypFC.txt final_lcblypFC.txt final_qtp00FC.txt final_qtp01FC.txt final_qtp02FC.txt final_wb97xFC.txt

while read line
do
	cd $line
	pwd
	cat FC_camb3lypFINAL.txt >> ../final_camb3lypFC.txt
	echo "" >> ../final_camb3lypFC.txt

	cat FC_lcblypFINAL.txt >> ../final_lcblypFC.txt
	echo "" >> ../final_lcblypFC.txt

	cat FC_qtp00FINAL.txt >> ../final_qtp00FC.txt
	echo "" >> ../final_qtp00FC.txt

	cat FC_qtp01FINAL.txt >> ../final_qtp01FC.txt
	echo "" >> ../final_qtp01FC.txt

	cat FC_qtp02FINAL.txt >> ../final_qtp02FC.txt
	echo "" >> ../final_qtp02FC.txt

	cat FC_wb97xFINAL.txt >> ../final_wb97xFC.txt
	echo "" >> ../final_wb97xFC.txt



	cd ../
done < dirListing.txt
