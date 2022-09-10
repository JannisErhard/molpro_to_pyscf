#
# Jannis Erhard <jannis.erhard@fau.de>
#

'''
A Script that reads an fcidump file, runs scf, runs FCI, then returns a density matrix compatible with molpro
'''



import psutil
import pyscf
from math import sqrt
from pyscf import tools
from pyscf import __config__
from utils import write_matrop, read_orbitals 
import numpy as np

MAX_MEMORY = getattr(__config__, 'MAX_MEMORY')
print(MAX_MEMORY)


#print(psutil.virtual_memory())

print("\nNumber of OMP threads =", pyscf.lib.num_threads())
print(pyscf.__file__)
print(pyscf.__version__)


myhf = tools.fcidump.to_scf('fcidump', molpro_orbsym=False, mf=None)
print(f"myhf.mo_occ")
myhf.run()


debug = False

if debug:
    dm = myhf.make_rdm1()
    print("This is the HF DM")
    print(dm)

# create an FCI solver based on the SCF object
cisolver = pyscf.fci.FCI(myhf)
cisolver.conv_tol = 1e-9


e, fcivec = cisolver.kernel(verbose=5)
print(f"E={e}")


norb = myhf.mo_coeff.shape[1]

if debug:
    # show contents of scf object
    for element in dir(myhf):
        print(element, getattr(myhf,element))

# 6 alpha electrons, 4 beta electrons because spin = nelec_a-nelec_b = 2
nelec_a = 2
nelec_b = 2
dm1 = cisolver.make_rdm1(fcivec, norb, (nelec_a,nelec_b))
orbitals = read_orbitals('Test_File')
dm_molpro = np.matmul(np.matmul(orbitals,dm1), orbitals.transpose())


debug = True 
if debug:
    print("Density Matrix From PySCF")
    print(dm1)
    print("Density Matrix From Molpro")
    print(dm_molpro)

write_matrop('dm.txt',dm_molpro, norb)

