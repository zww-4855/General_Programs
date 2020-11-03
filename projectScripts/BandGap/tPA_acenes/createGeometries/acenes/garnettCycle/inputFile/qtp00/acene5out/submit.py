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
C 6.117721 0.716456 0.000000
C 6.117721 -0.716456 0.000000
H 7.065952 -1.247064 0.000000
H 7.065952 1.247064 0.000000
C 4.941657 1.410527 0.000000
C 4.941657 -1.410527 0.000000
C 3.678746 0.727647 0.000000
C 3.678746 -0.727647 0.000000
H 4.939919 2.498020 0.000000
H 4.939919 -2.498020 0.000000
C 2.467582 1.407836 0.000000
C 2.467582 -1.407836 0.000000
C 1.226500 0.728534 0.000000
C 1.226500 -0.728534 0.000000
H 2.467624 2.495998 0.000000
H 2.467624 -2.495998 0.000000
C -0.000028 1.408524 0.000000
C -0.000028 -1.408524 0.000000
C -1.226469 0.728539 0.000000
C -1.226469 -0.728539 0.000000
H -0.000017 2.496573 0.000000
H -0.000017 -2.496573 0.000000
C -2.467625 1.407846 0.000000
C -2.467625 -1.407846 0.000000
C -3.678713 0.727655 0.000000
C -3.678713 -0.727655 0.000000
H -2.467643 2.496006 0.000000
H -2.467643 -2.496006 0.000000
C -4.941671 1.410535 0.000000
C -4.941671 -1.410535 0.000000
C -6.117708 0.716482 0.000000
C -6.117708 -0.716482 0.000000
H -4.939849 2.498024 0.000000
H -4.939849 -2.498024 0.000000
H -7.065930 1.247100 0.000000
H -7.065930 -1.247100 0.000000
   
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

