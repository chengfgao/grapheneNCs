#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 9:41:20 2018

@author: frankgao
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import signal_smoothing as ss

my_path = os.path.abspath(__file__)

font = {'weight' : 'bold',
        'size'   : 18}
plt.rc('font', **font)

#Calculate the slab velocity-velocity autocorrelation function 
#The diameter of Argon is 3.76 Angstrom
#First layer of liquid molecule is around y=3.4+3.76=7.16 Angstrom 

#From Cuu calculation, a time average of slabnum has been obtained
slabnum = 78
nsample = 20000
N = 1200
#Empty array for velocity and y position
fxtraj = np.zeros(N)
ytraj = np.zeros(N)
velxtraj = np.zeros(N)

vxslabs1 = np.zeros(int(nsample))
fxslabs1 = np.zeros(int(nsample))
vxslabs2 = np.zeros(int(nsample))
fxslabs2 = np.zeros(int(nsample))
#track the index (nonphysical) of particle
global index
index = 0
global cursample
cursample = 0

#The calculation of vslabs and fxslabs
dataFile = open("All_EMD_info.dump", "r")
cursample = 0
for i, line in enumerate(dataFile):
    data = line.split(" ")
    if data[0] == 'ITEM:':
        if cursample > 0:
            #sort the friction array based on position array
            #Then use the "slabnum" amount of particles close to the graphene 
            #to find slab friction due to the wall
            fxslab1 = 0
            fxslab2 = 0
            #sort the velocity array based on position array
            #Then use the "slabnum" amount of particles close to the graphene 
            #to find slab velocities
            vxslab1 = 0
            vxslab2 = 0
            inds = ytraj.argsort()
            sortedfx = fxtraj[inds]
            sortedvelx = velxtraj[inds]
            for n in range(0, int(slabnum)):
                fxslab1 += sortedfx[n]  
                vxslab1 += sortedvelx[n]  
                fxslab2 += sortedfx[(-1*n)]  
                vxslab2 += sortedvelx[(-1*n)]                  
            fxslabs1[cursample-1] = fxslab1    
            vxslabs1[cursample-1] = vxslab1
            fxslabs2[cursample-1] = fxslab2    
            vxslabs2[cursample-1] = vxslab2       
        cursample += 1
        [next(dataFile) for skip in range(8)] 
    else:
        #Store fx then y
        ytraj[index] = data[0]
        velxtraj[index] = data[1]
        fxtraj[index] = data[2]
        index += 1
        if index == N:
            index = 0        
#Process the last set of data        
fxslab1 = 0
fxslab2 = 0
vxslab1 = 0
vxslab2 = 0
inds = ytraj.argsort()
sortedfx = fxtraj[inds]
sortedvelx = velxtraj[inds]
for n in range(0, int(slabnum)):
    fxslab1 += sortedfx[n]  
    vxslab1 += sortedvelx[n]  
    fxslab2 += sortedfx[(-1*n)]  
    vxslab2 += sortedvelx[(-1*n)]                  
fxslabs1[cursample-1] = fxslab1    
vxslabs1[cursample-1] = vxslab1
fxslabs2[cursample-1] = fxslab2    
vxslabs2[cursample-1] = vxslab2  
      
#Range of Correlation Function      
tauMax = 50
timeinterval = 500
times = np.linspace(0, (tauMax*timeinterval)/1000, tauMax)

#Calculate the VACF for the slab
Cuu1 = np.zeros(int(tauMax))
Cuu2 = np.zeros(int(tauMax))
for tau in range(0, int(tauMax)):
    for t in range(0, int(nsample-tauMax)):
        Cuu1[tau] += vxslabs1[t]*vxslabs1[t+tau]
        Cuu2[tau] += vxslabs2[t]*vxslabs2[t+tau]
Cuu = np.zeros(int(tauMax))     
for tau in range(0, int(tauMax)):
    Cuu[tau] = Cuu1[tau]+Cuu2[tau]
#norm = Cuu[0]
#for tau in range(0, int(tauMax)):
#    Cuu[tau] = Cuu[tau]/norm
#    

#Store the correlation function
#outFile = open('CuuData', 'w')
#for tau in range(0, int(tauMax)):
#    outFile.write(str(tau*timeinterval/1000))
#    outFile.write(' ')
#    outFile.write(str(Cuu[tau]))
#    outFile.write('\n')
#outFile.close()

#Calculate the Force Velocity cross correlation for the slab
Cuf1 = np.zeros(int(tauMax))
Cuf2 = np.zeros(int(tauMax))
for tau in range(0, int(tauMax)):
    for t in range(0, int(nsample-tauMax)):
        Cuf1[tau] += vxslabs1[t]*fxslabs1[t+tau]
        Cuf2[tau] += vxslabs2[t]*fxslabs2[t+tau]
adjust1 = Cuf1[0]
adjust2 = Cuf2[0]
for tau in range(0, int(tauMax)):
    Cuf1[tau] = Cuf1[tau]-adjust1
    Cuf2[tau] = Cuf2[tau]-adjust2
Cuf = np.zeros(int(tauMax))
for tau in range(0, int(tauMax)):
    Cuf[tau] = Cuf1[tau]+Cuf2[tau]
#norm = -1*np.amin(Cuf) 
#for tau in range(0, int(tauMax)):
#    Cuf[tau] = Cuf[tau]/norm
Cuf[7:50] = ss.savitzky_golay(Cuf[7:50], window_size = 41, order = 5)    

#Store the cross correlation function
#outFile = open('CufData', 'w')
#for tau in range(0, int(tauMax)):
#    outFile.write(str(tau*timeinterval/1000))
#    outFile.write(' ')
#    outFile.write(str(Cuf[tau]))
#    outFile.write('\n')
#outFile.close()

plt.plot(times, Cuu)
plt.plot(times, Cuf)
plt.xlabel(r"$\tau(ps)$")
plt.legend([r"$C_{uu}$", r"$C_{uF'_{x}}$"])
#plt.savefig('CF Plot.jpg',format='jpg', bbox_inches='tight', dpi=800)
plt.clf()


