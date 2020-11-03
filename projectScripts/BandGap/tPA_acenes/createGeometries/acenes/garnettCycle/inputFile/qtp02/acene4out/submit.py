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
C 4.889184 0.715267 0.000000
C 4.889184 -0.715267 0.000000
H 5.837094 -1.246479 0.000000
H 5.837094 1.246479 0.000000
C 3.711380 1.409387 0.000000
C 3.711380 -1.409387 0.000000
C 2.450840 0.725941 0.000000
C 2.450840 -0.725941 0.000000
H 3.709630 2.496931 0.000000
H 3.709630 -2.496931 0.000000
C 1.235427 1.406152 0.000000
C 1.235427 -1.406152 0.000000
C 0.000016 0.726124 0.000000
C 0.000016 -0.726124 0.000000
H 1.235305 2.494321 0.000000
H 1.235305 -2.494321 0.000000
C -1.235526 1.406147 0.000000
C -1.235526 -1.406147 0.000000
C -2.450799 0.725948 0.000000
C -2.450799 -0.725948 0.000000
H -1.235335 2.494309 0.000000
H -1.235335 -2.494309 0.000000
C -3.711407 1.409399 0.000000
C -3.711407 -1.409399 0.000000
C -4.889136 0.715307 0.000000
C -4.889136 -0.715307 0.000000
H -3.709510 2.496929 0.000000
H -3.709510 -2.496929 0.000000
H -5.837057 1.246476 0.000000
H -5.837057 -1.246476 0.000000
   
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

