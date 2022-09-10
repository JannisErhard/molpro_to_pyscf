#!/bin/python3
import sys
import numpy as np
from math import sqrt
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



def write_matrop(fname, mat, new_dim):
    mat2 = np.triu(mat)
    vector = mat[0,0]
    for i in range(1,new_dim):
        vector = np.append(vector, mat[:i+1,i])
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

