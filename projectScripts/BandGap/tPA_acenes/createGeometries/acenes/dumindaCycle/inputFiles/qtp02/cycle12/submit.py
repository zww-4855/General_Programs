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

H  0.0  1.23256  -1.577103
H  0.0  -1.23256  -1.577103
C  0.0  0.697583  -0.650443
C  0.0  -0.697583  -0.650443
C  0.0  -1.395038  0.557442
C  0.0  1.395038  0.557442
H  0.0  -2.494718  0.557442
H  0.0  2.494718  0.557442
C  0.0  0.697583  1.765326
C  0.0  -0.697583  1.765326
C  0.0  -1.395038  2.973211
C  0.0  1.395038  2.973211
H  0.0  -2.494718  2.973211
H  0.0  2.494718  2.973211
C  0.0  0.697583  4.181095
C  0.0  -0.697583  4.181095
C  0.0  -1.395038  5.38898
C  0.0  1.395038  5.38898
H  0.0  -2.494718  5.38898
H  0.0  2.494718  5.38898
C  0.0  0.697583  6.596864
C  0.0  -0.697583  6.596864
C  0.0  -1.395038  7.804749
C  0.0  1.395038  7.804749
H  0.0  -2.494718  7.804749
H  0.0  2.494718  7.804749
C  0.0  0.697583  9.012633000000001
C  0.0  -0.697583  9.012633000000001
C  0.0  -1.395038  10.220518
C  0.0  1.395038  10.220518
H  0.0  -2.494718  10.220518
H  0.0  2.494718  10.220518
C  0.0  0.697583  11.428402000000002
C  0.0  -0.697583  11.428402000000002
C  0.0  -1.395038  12.636287000000001
C  0.0  1.395038  12.636287000000001
H  0.0  -2.494718  12.636287000000001
H  0.0  2.494718  12.636287000000001
C  0.0  0.697583  13.844171000000001
C  0.0  -0.697583  13.844171000000001
C  0.0  -1.395038  15.052056
C  0.0  1.395038  15.052056
H  0.0  -2.494718  15.052056
H  0.0  2.494718  15.052056
C  0.0  0.697583  16.25994
C  0.0  -0.697583  16.25994
C  0.0  -1.395038  17.467824999999998
C  0.0  1.395038  17.467824999999998
H  0.0  -2.494718  17.467824999999998
H  0.0  2.494718  17.467824999999998
C  0.0  0.697583  18.675709
C  0.0  -0.697583  18.675709
C  0.0  -1.395038  19.883594000000002
C  0.0  1.395038  19.883594000000002
H  0.0  -2.494718  19.883594000000002
H  0.0  2.494718  19.883594000000002
C  0.0  0.697583  21.091478000000002
C  0.0  -0.697583  21.091478000000002
C  0.0  -1.395038  22.299363
C  0.0  1.395038  22.299363
H  0.0  -2.494718  22.299363
H  0.0  2.494718  22.299363
C  0.0  0.697583  23.507247000000003
C  0.0  -0.697583  23.507247000000003
C  0.0  -1.395038  24.715132000000004
C  0.0  1.395038  24.715132000000004
H  0.0  -2.494718  24.715132000000004
H  0.0  2.494718  24.715132000000004
C  0.0  0.697583  25.923016
C  0.0  -0.697583  25.923016
C  0.0  -1.395038  27.130901
C  0.0  1.395038  27.130901
H  0.0  -2.494718  27.130901
H  0.0  2.494718  27.130901
C  0.0  0.69758346  28.338785
C  0.0  -0.69758346  28.338785
H  0.0  1.23255993  29.2654322
H  0.0  -1.23255993  29.2654322                                                                ''',
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

