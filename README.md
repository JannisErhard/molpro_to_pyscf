# molpro_to_pyscf
Is taking input from molpro, runs calculations then churns out molpro compatible data. At this point density matrices.

# How to use:

First run molpro for your setup with input akin to this:

{hf; orbital,2100.2}
{matrop; load,orb; export,orb,orb.dat,status=rewind,prec=sci}
{FCI,dump=fcidump;core}

This will generate twi files. One called fcidump and one called orb.dat.

Now use this script in the following way:

...

This will generate a density matrix that is compatible with molpro frmo a PySCF FCI calulation.



# Tests
Tested Successfuly so far for:
1. Be sto3g FCI
2. Be aug-cc-pvdz FCI
