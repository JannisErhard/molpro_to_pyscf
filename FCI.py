#
# Jannis Erhard <jannis.erhard@fau.de>
#

'''
A Script that reads an fcidump file, runs scf, runs FCI, then returns a density matrix compatible with molpro
'''

def write_matrop(fname, mat):
    mat = mat.reshape(-1)
    new_dim = int(sqrt(mat.shape[0]))
    mat = mat.reshape(new_dim,new_dim)
    mat2 = np.triu(mat)
    print(mat)
    vector = mat[0,0]
    for i in range(1,new_dim):
        print(vector)
        print(mat[:i,i])
        vector = np.append(vector, mat[:i+1,i])
    for i in range(0,len(vector),3):
            print(i)
    #print(len(vector))
    with open(fname, 'w') as fin:
        fin.write('BEGIN_DATA,\n')
        if (len(vector)%3==0):
            for i in range(0,len(vector),3):
                fin.write("%25.15f, %25.15f, %25.15f,\n"%(vector[i], vector[i+1], vector[i+2]))
        if (len(vector)%3==1):
            for i in range(0,len(vector)-3,3):
                fin.write("%25.15f, %25.15f, %25.15f,\n"%(vector[i], vector[i+1], vector[i+2]))
            fin.write("%25.15f,\n"%vector[-1])
        if (len(vector)%3==2):
            for i in range(0,len(vector)-3,3):
                fin.write("%25.15f, %25.15f, %25.15f,\n"%(vector[i], vector[i+1], vector[i+2]))
            fin.write("%25.15f, %25.15f,\n"%vector[-2], vector[-1])
        fin.write('END_DATA,\n')


import psutil
import pyscf
from math import sqrt
from pyscf import tools
from pyscf import __config__
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
print(myhf.mo_coeff)


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
print(dm1)
write_matrop('dm.txt',dm1)

