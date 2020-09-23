#!/bin/bash
# radicalA/B.txt and expDataA/B.txt are constant input files containing relevant info for the data for the 1st or 2nd part of column info
# everything else are names of the corrected DFT FC files ONLY containg values w/o spaces 

#MUST PIPE THIS TO OUTPUT FILE IF CORRECT
# TEST OUTPUT FOR TABLE WORKS WHEN INSERTED INTO LATEX

paste radicalA.txt nucleiA.txt KLcopyA_copy_final_qtp00FC.txt KLcopyA_copy_final_qtp01FC.txt KLcopyA_copy_final_qtp02FC.txt expDataA.txt  radicalB.txt nucleiB.txt KLcopyB_copy_final_qtp00FC.txt KLcopyB_copy_final_qtp01FC.txt KLcopyB_copy_final_qtp02FC.txt expDataB.txt > temp.txt


awk '{printf "%s%s&%.1f&%.1f&%.1f&%.1f&%s%s&  %.1f  &  %.1f  &  %.1f  &  %.1f \\\\  \n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12}' temp.txt


