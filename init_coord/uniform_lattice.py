#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 10:18:51 2018

@author: frankgao
"""
import numpy as np

f = open('data34x34x41.argon', 'w')

X = 34.4
Y = 36.2 #Put atoms in to (6.80, 41) on y direction
Z = 34.4
#in LJ units the standard size is sigma=0.34nm x=10sigma, y=10sigma, z=15sigma

N = 964
LatScale = 0.9*Z/(np.rint(np.power(N, 1/3)))

i = 0
j = 0
k = 0
count = 0

def LatticePosition(scale):
    global i 
    global j 
    global k 
    global count 
    count = count + 1
    
    x = i*scale
    y = j*scale+6.80
    z = k*scale
    i = i+1 
    
    x = float("{0:.4f}".format(x))
    y = float("{0:.4f}".format(y))
    z = float("{0:.4f}".format(z))
    
    f.write(str(count+1792)+' '+ str(1)+' '+str(x)+' '+str(y)+' '+str(z))
    f.write('\n')
    
    if i*scale > X:
        i = 0
        j = j+1
        if j*scale > Y:
            j = 0
            k = k+1

for n in range(0, int(N)): 
    LatticePosition(LatScale)

