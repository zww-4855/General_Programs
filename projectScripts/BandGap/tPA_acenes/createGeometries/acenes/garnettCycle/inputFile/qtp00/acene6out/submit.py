#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

from pyscf import gto
from pyscf import scf
from pyscf import lib

'''
Density fitting method by decorating the scf object with scf.density_fit function.

There is no flag to control the program to do density fitting for 2-electron
integration.  The way to call density fitting is to decorate the existed scf
object with scf.density_fit function.

NOTE scf.density_fit function generates a new object, which works exactly the
same way as the regular scf method.  The density fitting scf object is an
independent object to the regular scf object which is to be decorated.  By
doing so, density fitting can be applied anytime, anywhere in your script
without affecting the exsited scf object.

See also:
examples/df/00-with_df.py
examples/df/01-auxbasis.py 
'''

lib.num_threads(44)
mol = gto.Mole()
mol.build(
    verbose = 7,
    atom = '''
C -7.350517 0.715773 0.000000
C -7.350517 -0.715773 0.000000
H -8.298142 -1.247504 0.000000
H -8.298142 1.247504 0.000000
C -6.172862 1.409775 0.000000
C -6.172862 -1.409775 0.000000
C -4.911467 0.727133 0.000000
C -4.911467 -0.727133 0.000000
H -6.170427 2.497230 0.000000
H -6.170427 -2.497230 0.000000
C -3.698398 1.407935 0.000000
C -3.698398 -1.407935 0.000000
C -2.457546 0.729346 0.000000
C -2.457546 -0.729346 0.000000
H -3.698513 2.496086 0.000000
H -3.698513 -2.496086 0.000000
C -1.232079 1.409756 0.000000
C -1.232079 -1.409756 0.000000
C 0.000001 0.730568 0.000000
C 0.000001 -0.730568 0.000000
H -1.232324 2.497778 0.000000
H -1.232324 -2.497778 0.000000
C 1.232076 1.409755 0.000000
C 1.232076 -1.409755 0.000000
C 2.457547 0.729345 0.000000
C 2.457547 -0.729345 0.000000
H 1.232315 2.497777 0.000000
H 1.232315 -2.497777 0.000000
C 3.698396 1.407933 0.000000
C 3.698396 -1.407933 0.000000
C 4.911470 0.727133 0.000000
C 4.911470 -0.727133 0.000000
H 3.698508 2.496084 0.000000
H 3.698508 -2.496084 0.000000
C 6.172863 1.409777 0.000000
C 6.172863 -1.409777 0.000000
C 7.350516 0.715771 0.000000
C 7.350516 -0.715771 0.000000
H 6.170439 2.497232 0.000000
H 6.170439 -2.497232 0.000000
H 8.298147 1.247490 0.000000
H 8.298147 -1.247490 0.000000
   
                                                                ''',
    unit='Angstrom',
    basis = 'ccpvtz',
    max_memory=10000,
)


#
# By default optimal auxiliary basis (if possible) or even-tempered gaussian
# functions are used fitting basis.  You can assign with_df.auxbasis to change
# the change the fitting basis.
#
mol.spin = 0
mol.charge = 0
mol.build(0, 0)
mf = scf.RKS(mol)
mf.xc='cam-b3lyp'
mf.define_xc_('0.91*LR_HF(0.29) + 0.54*SR_HF(0.29)+0.37*ITYH +0.09*B88, 0.80*LYP + .20*VWN','GGA', 0.91,(0.29,0.91, -0.37))
energy = mf.kernel()
mos=mf.mo_energy
print(mos)
print('mo occ: ',mf.mo_occ)
print('total num of electrons: ', sum(mf.mo_occ))
homoIndex=int(sum(mf.mo_occ)/2 - 1)
lumoIndex=homoIndex+1
bandGap=(mos[lumoIndex] - mos[homoIndex])*27.2114
print('index: ', homoIndex, lumoIndex)
print('homo E:',mos[homoIndex])
print('lumo E:', mos[lumoIndex])
print('band Gap (eV):', bandGap)

