#
# Jannis Erhard <jannis.erhard@fau.de>
#

'''
A Script that reads an fcidump file, runs scf, runs FCI, then returns a density matrix compatible with molpro
'''



import pyscf
import numpy as np
from pyscf import tools
from pyscf import __config__
from utils import write_matrop, read_orbitals 

MAX_MEMORY = getattr(__config__, 'MAX_MEMORY')
print(MAX_MEMORY)


#print(psutil.virtual_memory())

print("\nNumber of OMP threads =", pyscf.lib.num_threads())
print(pyscf.__file__)
print(pyscf.__version__)


myhf = tools.fcidump.to_scf('fcidump', molpro_orbsym=False, mf=None)
myhf.run()


# create an FCI solver based on the SCF object
cisolver = pyscf.fci.FCI(myhf)
cisolver.conv_tol = 1e-9


e, fcivec = cisolver.kernel(verbose=5)


norb = myhf.mo_coeff.shape[1]

# 6 alpha electrons, 4 beta electrons because spin = nelec_a-nelec_b = 2
dm1 = cisolver.make_rdm1(fcivec, myhf.mo_coeff.shape[0], myhf.mol.nelec)
orbitals = read_orbitals('Test_File')
dm_molpro = np.matmul(np.matmul(orbitals,dm1), orbitals.transpose())

print(f"E={e}")

write_matrop('dm.txt',dm_molpro, norb)

