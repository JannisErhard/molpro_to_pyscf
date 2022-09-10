#!/bin/python3
import numpy as np
def read_orbitals(filename, norbs):
    ''' reads any file containing a square matrix into an numpy squaree array'''
    with open(filename) as f:
        lines = f.readlines()
    coefficients = []
    for line in lines:
        entries = line.split()
        for entry in entries:
            coefficients.append(float(entry))
    orbitals = np.reshape(coefficients, (norbs, norbs))
    return orbitals



def write_matrop(fname, mat, new_dim):
    '''  takes matrix, extracts upper traingale, writes it in columns of 3 into file'''
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

def read_orbitals_from_record(filename, norbs):
    ''' Reads Molpro record file and parses Orbitals intpó matrix'''
    with open(filename) as f:
        lines = f.readlines()
    words = []
    for line in lines:
        line.replace('D+','E+')
        for word in line.replace(',','').replace('D+','E+').replace('D-','E-').split():
            words.append(word)
    start = words.index("ORBITALS")+7
    end = words.index('EIG')
    orbitals = np.reshape(np.array(words[start:end]), (norbs, norbs)).astype(float).transpose()
    return orbitals
