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
C -12.286459 0.713204 0.000000
C -12.286459 -0.713204 0.000000
H -13.232858 -1.247136 0.000000
H -13.232858 1.247136 0.000000
C -11.104552 1.407441 0.000000
C -11.104552 -1.407441 0.000000
C -9.848699 0.724254 0.000000
C -9.848699 -0.724254 0.000000
H -11.102098 2.494931 0.000000
H -11.102098 -2.494931 0.000000
C -8.626957 1.405881 0.000000
C -8.626957 -1.405881 0.000000
C -7.395009 0.727344 0.000000
C -7.395009 -0.727344 0.000000
H -8.627386 2.494068 0.000000
H -8.627386 -2.494068 0.000000
C -6.158121 1.408266 0.000000
C -6.158121 -1.408266 0.000000
C -4.934211 0.730243 0.000000
C -4.934211 -0.730243 0.000000
H -6.158802 2.496330 0.000000
H -6.158802 -2.496330 0.000000
C -3.693580 1.409318 0.000000
C -3.693580 -1.409318 0.000000
C -2.468192 0.731552 0.000000
C -2.468192 -0.731552 0.000000
H -3.693840 2.497387 0.000000
H -3.693840 -2.497387 0.000000
C -1.231033 1.409431 0.000000
C -1.231033 -1.409431 0.000000
C -0.000005 0.731841 0.000000
C -0.000005 -0.731841 0.000000
H -1.231077 2.497521 0.000000
H -1.231077 -2.497521 0.000000
C 1.231025 1.409431 0.000000
C 1.231025 -1.409431 0.000000
C 2.468184 0.731552 0.000000
C 2.468184 -0.731552 0.000000
H 1.231052 2.497521 0.000000
H 1.231052 -2.497521 0.000000
C 3.693573 1.409317 0.000000
C 3.693573 -1.409317 0.000000
C 4.934206 0.730244 0.000000
C 4.934206 -0.730244 0.000000
H 3.693823 2.497385 0.000000
H 3.693823 -2.497385 0.000000
C 6.158118 1.408263 0.000000
C 6.158118 -1.408263 0.000000
C 7.395010 0.727345 0.000000
C 7.395010 -0.727345 0.000000
H 6.158798 2.496327 0.000000
H 6.158798 -2.496327 0.000000
C 8.626961 1.405879 0.000000
C 8.626961 -1.405879 0.000000
C 9.848706 0.724254 0.000000
C 9.848706 -0.724254 0.000000
H 8.627398 2.494066 0.000000
H 8.627398 -2.494066 0.000000
C 11.104563 1.407439 0.000000
C 11.104563 -1.407439 0.000000
C 12.286471 0.713205 0.000000
C 12.286471 -0.713205 0.000000
H 11.102124 2.494928 0.000000
H 11.102124 -2.494928 0.000000
H 13.232869 1.247141 0.000000
H 13.232869 -1.247141 0.000000
   
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

