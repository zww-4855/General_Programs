#!/usr/bin/env python
# coding: utf-8
# Assumes all geometry files, ref. input (.inp & .sh) files,
# and parse file are in the same directory
# Program syntax: HarvestOptCoords.py -d "opt geo directory path" -i "reference input file for FC"
#                                   -f "ACES/ORCA"
# opt geo directory path - path where all directories lie that contain
#                           optimized coordinates
# reference input file for FC - FC input file in cwd (whereever you call this program) that has &charge, &mult, 
#                                   &coords, &atom which this program will replace with the relevant values after harvesting
#
#last part - Necessary to obtain charge/mult dpending on whether optimization was done in ACES or ORCA
#
# How To Run Program: 
#       1) Go to empty directory where you want to create folders
#           to run FC info
#       2) Use above command
#
#       NEEDS IN CWD: FC reference input file
#
#       ONLY WORKS FOR ORCA INPUT/OUTPUT FILES!!! 
#       NEED TO RUN BASH SCRIPT TO CHANGE THE SUB NAME IN
#       THE SUBMISSION SCRIPT TO: '*dirName*_FC.inp'
#       WHERE *dirName* is the name of the newly created parent dir 
#
# PROGRAM GOAL: HARVEST OPT COORDS, CHARGE, AND MULT. FROM .xyz FILE AND INSERT INTO SHELL FILE
#               WORKS/TESTED ON ACES AND ORCA SHELL FILES. 
#               OPT COORD .xyz FILE MUST BE IN THE ORCA .xyz FROMAT
#               OR ACES2/III Format
import collections
import os
import subprocess
import math
from decimal import *
import re
import sys
import getopt



def main():
    cwd=os.getcwd() #current directory in which all new files/folders will be created
    fullCmdArgs=sys.argv
    print("full cmd", fullCmdArgs)
    argList=fullCmdArgs[1:]
    print("arg list:", argList)
    unixOptions="hd:i:f:o:"
    gnuOptions=["help", "directory","input","format"]
    try:
        arguments,values=getopt.getopt(argList, unixOptions, gnuOptions)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    COMMAND=open('ref_command.txt','w')
    COMMAND.write(str(fullCmdArgs))
    COMMAND.close()
    print("arguement:", arguments,values)
    for curArg, curVal in arguments:
        if curArg in ("-h", "--help"):
            print("See program heading")
            print("Syntax is: *CreateFCinfile.py -d &optGeoDir& -i &reference ORCA FC infile& -f &formating for input file ORCA/ACES2")
            sys.exit(2)
        elif curArg in ("-d", "--directory"):
            geoWorkDir=curVal #NOT cwd, but the directory containing folders w/ optimized coords
        elif curArg in ("-i","--input"):
            FCinput=curVal
        elif curArg in ("-f","--format"):
            print("curArg curval", curArg, curVal)
            if curVal not in ['ORCA','ACES']: #WORKED B4 ADDED THIS LINE
                print("Necessary to specify the format file in order to harvest charge and multiplicity")
                print("See help for instructions")
                print(curVal)
                sys.exit(2)
            mult_chargeFormat=curVal  # extracts the mult and charge from ORCA or ACES ZMAT file

    print("mult and charge format file is: ", mult_chargeFormat)
    print("REFERENCE FC INPUT FILE:",FCinput)
    print(geoWorkDir)    
    opt_Dirs, optCoordPath=getOptCoordDirName(geoWorkDir, cwd)
    print('OPT dirs IS:::',opt_Dirs)
    print(optCoordPath)
    for i in range(len(opt_Dirs)):
        print()
        print("I IS:::", i)
        print(i,optCoordPath[i],opt_Dirs[i])
        charge,mult,endpath=create_Copy_Dirs(optCoordPath[i],opt_Dirs[i],cwd,FCinput,mult_chargeFormat)
        uniqueLetter,coords=harvestOptCoords(endpath,opt_Dirs[i]+'.xyz', 'orca')
        print(coords)
        print('unique letter is:',uniqueLetter)
        insertFCinfile(opt_Dirs[i],FCinput,coords,charge,mult,uniqueLetter)


#gets optimized coord. directory names
# found inside the '-d' portion of run command
def getOptCoordDirName(geoWorkDir,cwd):
    os.chdir(geoWorkDir)#inside directory with optimized coords
    print(os.getcwd())
    cwd_Dirs = filter(os.path.isdir, os.listdir(os.curdir)) #lists directories in cwd
    redo_cwdDirs=[]
    optCoordPath=[]
    print(cwd_Dirs)
    for i in cwd_Dirs:
        if '.ipynb_checkpoints' in i:
            continue
        redo_cwdDirs.append(i)
        optCoordPath.append(os.getcwd()+'/'+i)
    opt_Dirs=redo_cwdDirs
    os.chdir(cwd)
    return opt_Dirs,optCoordPath

#creates directories inside 'cwd' using input from 'getOptCoordDirName'
#Copies over relevant information to extract geometry optimization input file
# (*.inp), resulting optimized coords (*.xyz), and submission script (*.sh)
def create_Copy_Dirs(optCoordPath,opt_Dirs,cwd,FCinfile,formatFile):
    endpath=cwd+'/'+opt_Dirs
    FCinfile=cwd+'/'+FCinfile
    try:
        os.mkdir(endpath)
    except:
        print("directory already created")
    cmd='cp '+FCinfile+' '+endpath
    os.system(cmd)

    directory=optCoordPath+'/'
    optXYZcoords=directory+opt_Dirs+'.xyz'
    subScript=directory+opt_Dirs+'.sh'
    inputFileName=directory+opt_Dirs+'.inp'
    copyList=[optXYZcoords,subScript]#,inputFileName]
    #copyList=[subScript,inputFileName]
    for j in copyList:
        copyFiles=j
        cmd='cp '+copyFiles +' '+ endpath
        print(j,copyFiles)
        os.system(cmd)
    if formatFile == "ACES":
        inputFileName=directory+'ZMAT'
        cmd='cp '+inputFileName+' '+ endpath
        os.system(cmd)
    # return charge and multiplicity
    charge,mult=getCharge_Mult(inputFileName, formatFile)
    return charge,mult,endpath

def getCharge_Mult(inFile,formatFile):
    print("infile is named: ", inFile)
    if formatFile == "ORCA":
        with open(inFile, 'rw+') as filehandle:
            fileContent=filehandle.readlines()
            for line in fileContent:
                line=line.split()
                print(line)
                if '*' in line:
                    if 'xyz' in line:
                        charge=line[2]
                        mult=line[3]
                        print('CHARGE AND MULT',charge, mult)
    elif formatFile == "ACES":
        print('we have an EXCEPTION')
        print('***************')
        with open(inFile, 'rw+') as filehandle:
            fileContent=filehandle.readlines()
            for line in fileContent:
                newline=line.split(',')
                for sline in newline:
                    searchString=sline.split('=')
                    print("searchString is: ", searchString)
                    if 'mult' in searchString:
                        print('inside mult')
                        mult=searchString[1].strip('\n')
                    if 'charge' in searchString:
                        print('inside charge')
                        charge=searchString[1].split(')')
                        charge=charge[0]
    return charge,mult
        
# Reads the optimized .xyz coordinates, and the unique atomName
# for input into FC input file
def harvestOptCoords(optPathName,optFile, elecStructRefFile):
    os.chdir(optPathName)
    optCoords=[]
    if elecStructRefFile=='orca':
        try:
            with open(optFile, 'rw+') as filehandle:
                fileContent=filehandle.readlines()
                numberCoordLines=int(fileContent[0])
                for line in fileContent[2:]:
                    optCoords.append([line])
                #first find how many unique atoms
            uniqueLetter=[]
            with open(optFile,'r') as filehandle:
                fileContent=filehandle.readlines()
                for line in fileContent[2:]:
                    line=line.split()
                    if line[0] not in uniqueLetter:
                        uniqueLetter.append(line[0])
            print(uniqueLetter)

        except:
            print('not directory')
    return uniqueLetter, optCoords


def insertFCinfile(opt_Dirs,refFCinfile,optCoords,charge,mult,uniqueLetter):
    FCinfileName=opt_Dirs+'_FC.inp'
    #cmd='cp '+refFCinfile+' '+FCinfileName
    #os.system(cmd)
    print("REF INFILE IS:::***'", refFCinfile)
    outFile=open(FCinfileName,'w')
    with open(refFCinfile, 'rw+') as filehandle:
        fileContent=filehandle.readlines()
        for line in fileContent:
            print("REF FILE LINE:", line)
            if '&charge' in line or '&mult' in line:
                line=line.replace('&charge', charge)
                line=line.replace('&mult', mult)
                print(line)
                outFile.write(line)
                
            elif '&coords' in line:
                for x in range(len(optCoords)):
                    tempStr="".join(optCoords[x])
                    outFile.write(tempStr)
            
            elif '&nuclei' in line:
                inString='Nuclei= all &nuclei { aiso }'
                print('instring: ',inString)
                for letter in uniqueLetter:
                    print('letter',letter.split()[0])
                    newline=inString.replace('&nuclei', letter.split()[0])
                    outFile.write(newline+'\n')
            else:
                outFile.write(line)



main()

