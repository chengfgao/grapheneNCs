# -*- coding: utf-8 -*-
"""
Created on Wed May 30 19:14:11 2018

@author: Frank Gao
"""
import numpy as np
import matplotlib.pyplot as plt

#allfiles = ['4E_7.flow', '6_955E_7.flow', '6_975E_7.flow', '7E_7.flow',
#          "try2E_6.flow", "try3E_6.flow", '4E_6.flow']
#
#lfiles = ['6E_7.flow','6_5E_7.flow', '6_75E_7.flow', '6_85E_7.flow' , '7E_7.flow',
#          '6_955E_7.flow', '6_975E_7.flow', '4E_7.flow','4E_6.flow']
#'4E_6.flow', '4E_7.flow']

allfiles = ['3E10.flow', '4E10.flow']

for filename in allfiles:
    dataFile = open(filename, "r")
    count = 0
    nsample = 10000
    totalTime = np.linspace(10000000, 10000000+nsample*500, nsample)
        
    avgVxs = np.zeros(nsample)
    N = 1200
    cursample = 0
    
    for i, line in enumerate(dataFile):
            data = line.split(" ")
            if data[0] == 'ITEM:':
                if cursample > 0:
                    avgVxs[cursample-1] = avgVxs[cursample-1]/N
                
                cursample += 1
                [next(dataFile) for skip in range(8)] 
            else:
                vx = float(data[1])
                avgVxs[cursample-1] += vx
    #Process the last data set             
    avgVxs[nsample-1] = avgVxs[nsample-1]/N
    
    
    tAvgVxs = np.zeros(nsample)
    for t in range(0, nsample):
        vxs = avgVxs[0:t]
        tAvg = np.trapz(vxs, dx=1)
        tAvgVxs[t] = tAvg/t
    
    #Average at each time
#    plt.plot(totalTime, avgVxs)
    
    #time average
    plt.plot(totalTime, tAvgVxs)

#plt.ylim(ymin = 0)
#plt.ylim(ymax = 35)
plt.xlabel('timestep')
plt.ylabel(r"$u_x$")
plt.title('Time Avearge of Velocity')
plt.savefig('timeAvg.png', bbox_inches = 'tight')
plt.show()