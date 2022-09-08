#!/bin/python3
import sys
import numpy as np
def read_orbitals(filename):
    with open(filename) as f:
        lines = f.readlines()
    norbs = len(lines[0].split())
    orbitals = np.empty([norbs, norbs])
    for i,line in enumerate(lines):
        entries = line.split()
        current_orbital = []
        for entry in entries:
            current_orbital.append(float(entry))
        orbitals[i,:] = np.array(current_orbital)
    return orbitals

filename = sys.argv[1]
orbitals = read_orbitals(filename)
print(orbitals)




