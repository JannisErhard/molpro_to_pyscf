#
# Jannis Erhard <jannis.erhard@fau.de>
#

'''
A Script that reads an fcidump file, runs scf, runs FCI, then returns a density matrix compatible with molpro
'''



from argparse import ArgumentParser
import pyscf
import numpy as np
from pyscf import tools
from pyscf import __config__
from utils import write_matrop, read_orbitals_from_record

MAX_MEMORY = getattr(__config__, 'MAX_MEMORY')
print(MAX_MEMORY)


print("\nNumber of OMP threads =", pyscf.lib.num_threads())
print(pyscf.__file__)
print(pyscf.__version__)


parser = ArgumentParser()
parser.add_argument("-rf","--record_file",dest="record_file",help="Molpro generated file that contains dump record")
parser.add_argument("-ff","--fcidump_file",dest="fcidump_file",help="Molpro generated fcidump file")
parser.add_argument("-of","--output_file",dest="outfile",help="File in which Molpro compatible density matrix information is stored")
args = parser.parse_args()


# read integrals from fcidumpfile which generates SCF object,  then generate orbitals by executing run method which updates SCF object
myhf = tools.fcidump.to_scf(args.fcidump_file, molpro_orbsym=False, mf=None)
myhf.run()


# create a cisolver object based on the SCF object an execute the CI algorithm
cisolver = pyscf.fci.FCI(myhf)
cisolver.conv_tol = 1e-9
e, fcivec = cisolver.kernel()



# 
dm1 = cisolver.make_rdm1(fcivec, myhf.mo_coeff.shape[0], myhf.mol.nelec)
#orbitals = read_orbitals(test+'orbfile',myhf.mo_coeff.shape[0])
orbitals = read_orbitals_from_record(args.record_file,myhf.mo_coeff.shape[0])


dm_molpro = np.matmul(np.matmul(orbitals,dm1), orbitals.transpose())
print(f"E={e}")

write_matrop(args.outfile,dm_molpro, myhf.mo_coeff.shape[0])
