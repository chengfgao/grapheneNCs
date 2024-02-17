#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 16:52:52 2019

@author: frankgao
"""

import numpy as np
import matplotlib as plt
from scipy import io

mat_name = ''
nsample = 200000
dt = 2
bts = ['9', '24', '39']
vxts = io.loadmat(mat_name)

vxt_Avgs = np.zeros((3, nsample))
for i in range(len(bts)):
    vxt = vxts[bts[i]]
    for j in range(nsample):
        if j == 0:
            vxt_Avgs[i][j] = 0
        else:
            vxt_Avgs[i][j] = np.trapz(vxt[0:j], dx=2)/(j*dt)

vxt_Avg_errs = np.zeros((3, nsample))
for i in range(len(bts)):
    vxt_Avg = vxt_Avgs[i,:]
    vxtFinal = vxt_Avg[-1]
    for j in range(nsample):
        vxt_Avg_errs[i][j]= np.abs(vxt_Avg[j]-vxtFinal)

t = np.linspace(0, nsample*dt, num=nsample)

for i in range(len(bts)):
    vxt_Avg_err = vxt_Avg_errs[i,:]
    plt.plot(t, vxt_Avg_err)

plt.xlabel('t')
plt.ylabel('Err')
plt.yscale('log')
    