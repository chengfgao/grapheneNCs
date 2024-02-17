# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 20:12:08 2018

@author: User
"""
import numpy as np
from scipy import io

allfiles = ['34x34x51_K=2_3E10']
#Specify "xz"-the wall dimension, "yl"-the channel width, "bins"-the number of bins
filenum = 0
xz=10
yl=51
N = 1200
nsample = 800000
bins = 50
#record bins of interest
bts = [5, 15, 24]

for filename in allfiles:
    afilename = filename + '.flow'
    dataFile = open(afilename, "r")
    count = 0
    
    bindiff = yl/bins
    yvals = np.linspace(-yl/20, yl/20, num=bins)
    #find the bin volume and start an array for density/velocity profile
    binVolume = (bindiff/3.4)*xz*xz
    rho = np.zeros(np.size(yvals))
    uxAvg = np.zeros(np.size(yvals))
    
    ux_t = np.zeros((3, nsample))
    
    for i, line in enumerate(dataFile):
            data = line.split(" ")
            if data[0] == 'ITEM:':
                if count > 0:
                    #record the ux(t)
                    for i in range(len(bts)):
                        ux_t[i][count] = uxAvg[bts[i]]/rho[bts[i]]
                [next(dataFile) for skip in range(8)] 
            else:
                ys = float(data[1])
                uxs = float(data[3])*100
                #Find the bin particle belongs to
                bin = np.floor((ys-3.4)/bindiff)
                bin = int(bin)
                if bin > bins:
                    bin = bin-1
                #Update the density and velocity bins
                rho[bin] = rho[bin]+1
                uxAvg[bin] = uxAvg[bin]+uxs
                
    #Normalize velocity bins
    for n in range(0, int(np.size(yvals))):
        if rho[n] == 0:
            uxAvg[n] = 0
        else:
            uxAvg[n] = uxAvg[n]/rho[n]  
    #Normalize density bins
    rho = rho/binVolume/nsample
    
    #Store the velocity and density Profile
    vString = filename + '_vp'
    rString = filename + '_rho'
    io.savemat(vString, {'51_bins=50_vp':uxAvg})
    io.savemat(rString, {'51_bins=50_rho':rho})

    io.savemat('51_bins_uxt', {str(bts[0]):ux_t[0,:]})
            
    
    filenum += 1
 






    
    
    
    
 