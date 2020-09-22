import numpy as np
### PURPOSE::: Convert Basis Set input file from EMSL library from CFOUR to ACESII/III format
###            Store EMSL information into "input.txt"
###            User needs to provide the atoms and respective basis set under the "baskey" 
###             identifier
###            Results are written to "output.txt"
###
def get_prim_cont(f2,str0,ltype):
    if (ltype=="prim") : nline=5
    if (ltype=="cont") : nline=7

    num1=len(str0)%nline
    num2=(len(str0)-num1)/nline
    ind=0
    for i in range(num2):
        str1=""
        for j in range(ind,ind+nline):
            if (ltype=="prim") : str2=("%14.7f"  % float(str0[j].replace("D","E")))
            if (ltype=="cont") : str2=("%10.7f " % float(str0[j].replace("D","E")))
            str1=str1+str2
        ind=ind+nline
        f2.write(str1+"\n")

    if (num1>=1):
        str1=""
        for j in range(ind,ind+num1):
            if (ltype=="prim") : str2=("%14.7f"  % float(str0[j].replace("D","E")))
            if (ltype=="cont") : str2=("%10.7f " % float(str0[j].replace("D","E")))
            str1=str1+str2
        ind=ind+num1
        f2.write(str1+"\n")


def read_cfour(info):
    finp=info["finp"]
    fout=info["fout"]
    baskey=info["baskey"]

    print("\n ***  transformation start  *** \n")

    f1=open(finp,'r')
    lines=f1.readlines()
    f1.close()

    lread=False
    for i in range(len(lines)):
        if (baskey==lines[i].strip()):
           ind=i
           break

    f2=open(fout,'w')

    #keyword/title 
    print(" *  basis-set key / title  ")
    print("---------------------------")
    for i in range(ind,ind+3):
        print('i is: ', i)
        f2.write(lines[i])
        print("    "+str(lines[i].strip()))
    ind=ind+3

    #information for blocks
    for i in range(ind,ind+5):
        f2.write(lines[i])
    totang=int(lines[ind])
    ang=lines[ind+1].split()
    cont=lines[ind+2].split() #contraction
    prim=lines[ind+3].split() #primitive
    ind=ind+5

    #primitive & contraction
    print(" *  basis-set blocks       ")
    print("---------------------------")
    print("   No.      l  prim.  cont.")
    for i in range(totang):
        ang0=int(ang[i])
        prim0=int(prim[i])
        cont0=int(cont[i])
        print("%5d : %5d  %5d  %5d" % (i,ang0,prim0,cont0))
        str0=lines[ind].split()
        get_prim_cont(f2,str0,'prim')
        f2.write("\n")
        ind=ind+2

        for j in range(prim0):
            str0=lines[ind].split()
            get_prim_cont(f2,str0,'cont')
            ind=ind+1
        f2.write("\n")
        ind=ind+1

    f2.close()

    print("\n ***  transformation end  *** \n")


def input():
    info={
      "finp": "input.txt",
      "fout": "output.txt",
      #"baskey": "I:cc-pVTZ-PP"
      "baskey":"S:aug-cc-pCVTZ"
    }
    return info

info=input()
read_cfour(info)

