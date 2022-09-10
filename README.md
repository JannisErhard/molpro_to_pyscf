# molpro_to_pyscf
Is taking input from molpro, runs calculations then churns out molpro compatible data. At this point density matrices.

# TODO - two
- [x] run from small fcidump
- [x] use read to get orbitals
- [x] use other function to transform
- [x] use special print to print to dm
- [x] paste special into heck-mack
- [x] compare dm-s 
- [x] run inversion, compare results 

# TODO - three 
- [x] get large orbital matrix
- [x] run from large dump 
- [x] repeat steps 3 to 8 

# TODO - meta 
- [ ] consider a way to print most of the heck-mack data 
- [ ] find a way to print spin matrices
- [x] write other function to transform
- [x] write function to read generic molpro record file to get orbitals

# Tests
1. Be sto3g 
2. Be aug-cc-pvdz
