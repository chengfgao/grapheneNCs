#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:36:06 2019

@author: frankgao
"""

import numpy as np
from scipy import io
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit

#bins = 24
#yl = 27.8
#yvals = io.loadmat('21_TG_Self_K=002_eta=1ps_KE_Traj1_rho')['ys'].ravel()

#def vp():
#    b = 3
#    uxAvg = io.loadmat('34x34x51_K=2_3E10_vp')['51_bins=50_vp'].ravel()
#    y = yvals[b:-(b)]
#    ux = uxAvg[b:-(b)]
#    plt.scatter(y, ux)
#    
##    p = np.polyfit(y, uxAvg, 2)
##    pred= p[0]*np.power(yvals, 2)+p[1]*yvals+p[2]
#    
#    #fit to y = a*y^2 + c
#    def predFunc(y, a, c):
#        return a*y*y+c
#    #guess for the param a and c
#    fpar, fCov = curve_fit(predFunc, y, ux)
#    pred = fpar[0]*np.power(y, 2)+fpar[1]
#    
#    plt.plot(y, pred, color = 'r')
#    print(fpar)
#    print(fCov)
#    sv_L = np.abs(uxAvg[b]/(2*fpar[0]*yvals[b]))
#    sv_H = np.abs(uxAvg[-b]/(2*fpar[0]*yvals[-b]))
#    print((sv_L, sv_H))
#    
##    plt.ylim([0, 25])
#    plt.xlabel('y(nm)', fontsize=16)
#    plt.ylabel(r'$v_x(y)$ (m/s)', fontsize=16)
#    plt.title('51 Velocity Profile', fontsize=16)
#    plt.savefig('51_vp.jpg', format='jpg', bbox_inches='tight', dpi=800)
    
#plt.clf()
    
#def rho_plot():
#    rho = io.loadmat('21_TG_Self_K=002_eta=1ps_KE_Traj1_rho')['21_bins=24_rho'].ravel()
#    plt.scatter(yvals, rho)
#    plt.plot(yvals, rho)
#    plt.xlabel('y(nm)', fontsize=16)
#    plt.ylabel(r'$\rho$', fontsize=16)
#    plt.title('21 Density Profile Temperature Gradient', fontsize=16)
#    plt.savefig('21_rho_TG.jpg', format='jpg', bbox_inches='tight', dpi=800)
#    
#def vr():
#    b = 5
#    y = yvals[b:-(b)]
#    
#    uxAvg = io.loadmat('34x34x51_K=2_3E10_vp')['51_bins=50_vp'].ravel()
#    uxAvg = uxAvg[b:-(b)]/np.max(uxAvg)
#    plt.scatter(y , uxAvg, marker = 'o', color = 'r')
#    
#    rho = io.loadmat('34x34x51_K=2_3E10_rho')['51_bins=50_rho'].ravel()
#    rho= rho[b:-(b)]/np.max(rho)
#    plt.scatter(y, rho)
#    plt.plot(y, rho)
    
def KE_plot(matnames, field):
    total_navg = 5
    KEs = np.zeros((total_navg, 20+4))
    yvals = np.zeros((total_navg, 20+4))
    n = 0
    all_dKE1_dx = []
    all_dKE2_dx = []
    
    for matname in matnames:
        data = io.loadmat(matname)
        KEi = data[field]
        yvalsi = data['ys']
        navg = (data['navg'].ravel())[0]
        for j in range(navg):
            KE_ij = KEi[j]
            KEs[n] = KE_ij
            yvals_ij = yvalsi[j]
            yvals[n] = yvals_ij
            plt.scatter(yvals_ij, KE_ij)
            plt.plot(yvals_ij, KE_ij)
            #calculate dKE/dx
            dx1 = yvals_ij[1]-yvals_ij[2]
            dx2 = yvals_ij[-3]-yvals_ij[-2]
            all_dKE1_dx.append(np.abs((KE_ij[1]-KE_ij[2])/dx1))
            all_dKE2_dx.append(np.abs((KE_ij[-3]-KE_ij[-2])/dx2))
            n += 1
    plt.ylim([0.013, 0.018])
    plt.xlabel('y(nm)', fontsize=16)
    plt.ylabel('Kinetic Energy', fontsize=16)
    plt.title('21 KE Profile', fontsize=16)
    plt.savefig('21_KE_TG.jpg', format='jpg', bbox_inches='tight', dpi=500)
    plt.show()
    
    
    #picture of averages
    plt.clf()
    KE_avgs = np.mean(KEs, axis=0)
    KE_serr = np.std(KEs, axis=0) 
    yvals_avgs =np.mean(yvals, axis=0)
    yvals_serr = np.std(yvals, axis=0) 
    plt.errorbar(yvals_avgs, KE_avgs,xerr=yvals_serr, yerr=KE_serr, fmt='bo-')
#    plt.plot(yvals, KE_avgs, 'r-')
    plt.xlabel('y(nm)', fontsize=16)
    plt.ylabel('Kinetic Energy', fontsize=16)
    plt.title('21 KE Profile', fontsize=16)
    plt.savefig('21_AVG_KE_TG.jpg', format='jpg', bbox_inches='tight', dpi=500)
    
    
    #calculate average dKE/dx
    dKE1_dx_avgs = np.mean(all_dKE1_dx, axis=0)
    dKE1_dx_serr = np.std(all_dKE1_dx, axis=0)
    dKE2_dx_avgs = np.mean(all_dKE2_dx, axis=0)
    dKE2_dx_serr = np.std(all_dKE2_dx, axis=0)
    print(all_dKE1_dx)
    print(all_dKE2_dx)
    print((dKE1_dx_avgs, dKE1_dx_serr))
    print((dKE2_dx_avgs, dKE2_dx_serr))
    
    
       
#KE_plot(['21_TG_Self_K=002_eta=1ps_KE_Traj4-1_ke'],
#         '21_TG_Self_K=002_eta=1ps_KE_Traj2_ke'], '21_bins=24_ke')
#KE_plot(['21_TG=20K_Self_K=002_eta=01ps_KE_Traj4-1_ke'], '21_bins=24_ke')
    
    
    
#plot heat flux
def HF_plot(files, nsamp=15000000, dt=0.0005):
    times = np.linspace(0, nsamp, num=nsamp+1)*dt
    for f in files:
        dQ_total = np.zeros(nsamp+1)
        datafile = open(f, 'r')
            
        for i, line in enumerate(datafile):
            if i < 2:
                continue;
            data = line.split(' ')
            dQ_total[i-2] = float(data[1])
        
        
        plt.plot(times, np.abs(dQ_total))
    
    plt.legend(['Wall1=130K', 'Wall2=110K'], fontsize=16)
    plt.xlabel('times/ps', fontsize=16)
    plt.ylabel('dQ', fontsize=16)
    plt.savefig('dQ.jpg', format='jpg', bbox_inches='tight', dpi=300)
        
            
HF_plot(['21_TG=20_K=002_Wall1_eta=01ps_dQ_Traj4-1', '21_TG=20_K=002_Wall2_eta=01ps_dQ_Traj4-1'])
                    
    
    
    
    
    
    
    
    
    
    
    
    