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
C 9.822751 0.713143 0.000000
C 9.822751 -0.713143 0.000000
H 10.769689 -1.246217 0.000000
H 10.769689 1.246217 0.000000
C 8.640499 1.406976 0.000000
C 8.640499 -1.406976 0.000000
C 7.384570 0.724117 0.000000
C 7.384570 -0.724117 0.000000
H 8.636571 2.494304 0.000000
H 8.636571 -2.494304 0.000000
C 6.162609 1.405479 0.000000
C 6.162609 -1.405479 0.000000
C 4.929929 0.727469 0.000000
C 4.929929 -0.727469 0.000000
H 6.161034 2.493535 0.000000
H 6.161034 -2.493535 0.000000
C 3.694126 1.408421 0.000000
C 3.694126 -1.408421 0.000000
C 2.467559 0.730635 0.000000
C 2.467559 -0.730635 0.000000
H 3.692886 2.496398 0.000000
H 3.692886 -2.496398 0.000000
C 1.230750 1.409903 0.000000
C 1.230750 -1.409903 0.000000
C -0.000016 0.731730 0.000000
C -0.000016 -0.731730 0.000000
H 1.230172 2.497885 0.000000
H 1.230172 -2.497885 0.000000
C -1.230777 1.409902 0.000000
C -1.230777 -1.409902 0.000000
C -2.467583 0.730633 0.000000
C -2.467583 -0.730633 0.000000
H -1.230207 2.497883 0.000000
H -1.230207 -2.497883 0.000000
C -3.694139 1.408418 0.000000
C -3.694139 -1.408418 0.000000
C -4.929935 0.727466 0.000000
C -4.929935 -0.727466 0.000000
H -3.692907 2.496394 0.000000
H -3.692907 -2.496394 0.000000
C -6.162601 1.405476 0.000000
C -6.162601 -1.405476 0.000000
C -7.384554 0.724113 0.000000
C -7.384554 -0.724113 0.000000
H -6.161031 2.493529 0.000000
H -6.161031 -2.493529 0.000000
C -8.640472 1.406970 0.000000
C -8.640472 -1.406970 0.000000
C -9.822720 0.713143 0.000000
C -9.822720 -0.713143 0.000000
H -8.636541 2.494295 0.000000
H -8.636541 -2.494295 0.000000
H -10.769647 1.246231 0.000000
H -10.769647 -1.246231 0.000000
   
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
mf.define_xc_('1.00*LR_HF(0.335) + .28*SR_HF(0.335)+0.72*ITYH, 1.00*LYP ',  'GGA', 1.00,(0.335,1.00, -0.72))
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

