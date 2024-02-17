#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:36:06 2019

@author: frankgao
"""

import numpy as np
from scipy import io
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

bins = 50
yl = 51
yvals = np.linspace(-yl/20, yl/20, num=bins)

def vp():
    b = 3
    uxAvg = io.loadmat('34x34x51_K=2_3E10_vp')['51_bins=50_vp'].ravel()
    y = yvals[b:-(b)]
    ux = uxAvg[b:-(b)]
    plt.scatter(y, ux)
    
#    p = np.polyfit(y, uxAvg, 2)
#    pred= p[0]*np.power(yvals, 2)+p[1]*yvals+p[2]
    
    #fit to y = a*y^2 + c
    def predFunc(y, a, c):
        return a*y*y+c
    #guess for the param a and c
    fpar, fCov = curve_fit(predFunc, y, ux)
    pred = fpar[0]*np.power(y, 2)+fpar[1]
    
    plt.plot(y, pred, color = 'r')
    print(fpar)
    print(fCov)
    sv_L = np.abs(uxAvg[b]/(2*fpar[0]*yvals[b]))
    sv_H = np.abs(uxAvg[-b]/(2*fpar[0]*yvals[-b]))
    print((sv_L, sv_H))
    
#    plt.ylim([0, 25])
    plt.xlabel('y(nm)', fontsize=16)
    plt.ylabel(r'$v_x(y)$ (m/s)', fontsize=16)
    plt.title('51 Velocity Profile', fontsize=16)
    plt.savefig('51_vp.jpg', format='jpg', bbox_inches='tight', dpi=800)
    
#plt.clf()
    
def rho():
    rho = io.loadmat('34x34x51_K=2_3E10_rho')['51_bins=50_rho'].ravel()
    plt.scatter(yvals, rho)
    plt.plot(yvals, rho)
    plt.xlabel('y(nm)', fontsize=16)
    plt.ylabel(r'$\rho$', fontsize=16)
    plt.title('51 Density Profile', fontsize=16)
    plt.savefig('51_rho.jpg', format='jpg', bbox_inches='tight', dpi=800)
    
def vr():
    b = 5
    y = yvals[b:-(b)]
    
    uxAvg = io.loadmat('34x34x51_K=2_3E10_vp')['51_bins=50_vp'].ravel()
    uxAvg = uxAvg[b:-(b)]/np.max(uxAvg)
    plt.scatter(y , uxAvg, marker = 'o', color = 'r')
    
    rho = io.loadmat('34x34x51_K=2_3E10_rho')['51_bins=50_rho'].ravel()
    rho= rho[b:-(b)]/np.max(rho)
    plt.scatter(y, rho)
    plt.plot(y, rho)
    
vp()