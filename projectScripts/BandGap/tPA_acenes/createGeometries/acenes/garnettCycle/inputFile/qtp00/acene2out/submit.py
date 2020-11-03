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
C -2.433661 0.708302 0.000000
C -2.433661 -0.708302 0.000000
H -3.378045 -1.245972 0.000000
H -3.378045 1.245972 0.000000
C -1.244629 1.402481 0.000000
C -1.244629 -1.402481 0.000000
C -0.000077 0.717168 0.000000
C -0.000077 -0.717168 0.000000
H -1.242734 2.490258 0.000000
H -1.242734 -2.490258 0.000000
C 1.244779 1.402533 0.000000
C 1.244779 -1.402533 0.000000
C 2.433606 0.708405 0.000000
C 2.433606 -0.708405 0.000000
H 1.242448 2.490302 0.000000
H 1.242448 -2.490302 0.000000
H 3.378224 1.245662 0.000000
H 3.378224 -1.245662 0.000000
   
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

