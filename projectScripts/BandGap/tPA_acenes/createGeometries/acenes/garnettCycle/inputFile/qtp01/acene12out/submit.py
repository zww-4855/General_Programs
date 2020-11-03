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
C 0.000000 0.713394 -14.748836
C 0.000000 -0.713394 -14.748836
H 0.000000 -1.247003 -15.695358
H 0.000000 1.247003 -15.695358
C 0.000000 1.407812 -13.567476
C 0.000000 -1.407812 -13.567476
C 0.000000 0.724478 -12.311353
C 0.000000 -0.724478 -12.311353
H 0.000000 2.495327 -13.565332
H 0.000000 -2.495327 -13.565332
C 0.000000 1.406129 -11.090439
C 0.000000 -1.406129 -11.090439
C 0.000000 0.727443 -9.858013
C 0.000000 -0.727443 -9.858013
H 0.000000 2.494335 -11.091319
H 0.000000 -2.494335 -11.091319
C 0.000000 1.408422 -8.622060
C 0.000000 -1.408422 -8.622060
C 0.000000 0.730154 -7.397949
C 0.000000 -0.730154 -7.397949
H 0.000000 2.496493 -8.623496
H 0.000000 -2.496493 -8.623496
C 0.000000 1.409295 -6.157676
C 0.000000 -1.409295 -6.157676
C 0.000000 0.731224 -4.933174
C 0.000000 -0.731224 -4.933174
H 0.000000 2.497354 -6.159031
H 0.000000 -2.497354 -6.159031
C 0.000000 1.409130 -3.694724
C 0.000000 -1.409130 -3.694724
C 0.000000 0.731313 -2.466697
C 0.000000 -0.731313 -2.466697
H 0.000000 2.497221 -3.695817
H 0.000000 -2.497221 -3.695817
C 0.000000 1.408825 -1.231658
C 0.000000 -1.408825 -1.231658
C 0.000000 0.731245 0.000000
C 0.000000 -0.731245 0.000000
H 0.000000 2.496953 -1.232101
H 0.000000 -2.496953 -1.232101
C 0.000000 1.408825 1.231656
C 0.000000 -1.408825 1.231656
C 0.000000 0.731313 2.466696
C 0.000000 -0.731313 2.466696
H 0.000000 2.496953 1.232094
H 0.000000 -2.496953 1.232094
C 0.000000 1.409130 3.694722
C 0.000000 -1.409130 3.694722
C 0.000000 0.731224 4.933172
C 0.000000 -0.731224 4.933172
H 0.000000 2.497220 3.695808
H 0.000000 -2.497220 3.695808
C 0.000000 1.409294 6.157673
C 0.000000 -1.409294 6.157673
C 0.000000 0.730154 7.397947
C 0.000000 -0.730154 7.397947
H 0.000000 2.497353 6.159021
H 0.000000 -2.497353 6.159021
C 0.000000 1.408421 8.622058
C 0.000000 -1.408421 8.622058
C 0.000000 0.727443 9.858013
C 0.000000 -0.727443 9.858013
H 0.000000 2.496492 8.623487
H 0.000000 -2.496492 8.623487
C 0.000000 1.406129 11.090441
C 0.000000 -1.406129 11.090441
C 0.000000 0.724478 12.311358
C 0.000000 -0.724478 12.311358
H 0.000000 2.494334 11.091314
H 0.000000 -2.494334 11.091314
C 0.000000 1.407813 13.567482
C 0.000000 -1.407813 13.567482
C 0.000000 0.713394 14.748844
C 0.000000 -0.713394 14.748844
H 0.000000 2.495328 13.565332
H 0.000000 -2.495328 13.565332
H 0.000000 1.246998 15.695371
H 0.000000 -1.246998 15.695371
   
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
mf.define_xc_('1.00*LR_HF(0.31) + .23*SR_HF(0.31)+0.77*ITYH, .80*LYP + .20*VWN',  'GGA', 1.00,(0.31,1.00, -0.77))
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

