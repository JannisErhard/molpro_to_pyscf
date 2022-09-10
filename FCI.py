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


print("\nNumber of OMP threads =", pyscf.lib.num_threads())
print(pyscf.__file__)
print(pyscf.__version__)


test='Test_1/'

# read integrals from fcidumpfile which generates SCF object,  then generate orbitals by executing run method which updates SCF object
myhf = tools.fcidump.to_scf(test+'fcidump', molpro_orbsym=False, mf=None)
myhf.run()


# create a cisolver object based on the SCF object an execute the CI algorithm
cisolver = pyscf.fci.FCI(myhf)
cisolver.conv_tol = 1e-9
e, fcivec = cisolver.kernel(verbose=5)



# 
dm1 = cisolver.make_rdm1(fcivec, myhf.mo_coeff.shape[0], myhf.mol.nelec)
orbitals = read_orbitals(test+'orbfile',myhf.mo_coeff.shape[0])
dm_molpro = np.matmul(np.matmul(orbitals,dm1), orbitals.transpose())

print(f"E={e}")

write_matrop(test+'dm.txt',dm_molpro, myhf.mo_coeff.shape[0])

