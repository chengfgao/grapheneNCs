# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 20:12:08 2018

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt

font = {'weight' : 'bold',
        'size'   : 18}

#allfiles = ['4E_7.flow', '6_955E_7.flow', '6_975E_7.flow', '7E_7.flow',
#          "try2E_6.flow", "try3E_6.flow", '4E_6.flow']
##Problem with "try1E_6.flow"
#lfiles = [ '4E_6.flow', '4E_7.flow', '7E_7.flow', 
#          '6_955E_7.flow', '6_975E_7.flow']
#
#temp = ['7E_7.flow']
#ignored "try6E_7.flow", '6_5E_7.flow', '6_925E_7.flow', 
#'6_75E_7.flow', '6_85E_7.flow', "try8E_7.flow"

allfiles = ['1E10.flow', '2E10.flow', '3E10.flow', '4E10.flow', '5E10.flow',
            '6E10.flow', '7E10.flow', '8E10.flow', '9E10.flow', '1E11.flow']

adjustFiles1 = ['3E10.flow', '4E10.flow']
smallFiles = ['1E10.flow', '2E10.flow', '9E10.flow', '6E10.flow', '8E10.flow']
midFiles = ['7E10.flow', '5E10.flow']

#Store the polynomial fit parameters
fitparams = np.zeros((len(allfiles), 3))
#Store the slip velocities (velocity at the boundary) of each trajectory (both ends)
slipVs = np.zeros((len(allfiles), 2))
#store the yw of each trajectory (both ends)
yws = np.zeros((len(allfiles), 2))

filenum = 0
for filename in allfiles:

    dataFile = open(filename, "r")
    count = 0
    nsample = 20000
    
    if filename in smallFiles:
        nsample = 5000
    if filename in midFiles:
        nsample = 10000

    N = 1200
    y = np.zeros(int(N*nsample))
    uxs = np.zeros(int(N*nsample))
    
    for i, line in enumerate(dataFile):
            data = line.split(" ")
            if data[0] == 'ITEM:':
                 [next(dataFile) for skip in range(8)] 
            else:
                y[count] = data[0]
                uxs[count] = data[1]
                count = count+1
     
        
    ymin = np.min(y)
    ymax = np.max(y)
    bins = 50

    bindiff = (ymax-ymin)/bins
    yvals = np.linspace((ymin-28.9)/10, (ymax-28.9)/10, num=bins)
    nsample = count/N
    
    
#    #Density Profile
#    binVolume = (bindiff/3.4)*10*10
#    rho = np.zeros(np.size(yvals))
#     
#    t1 = 0
#    while t1 < count:
#        bin = np.floor((y[t1]-ymin)/bindiff)
#        bin = int(bin)
#        rho[bin-1] = rho[bin-1]+1   
#        t1 += 1
#         
#    n1 = 0
#    while n1 < np.size(yvals):
#        rho[n1] = rho[n1]/binVolume/nsample 
#        n1 +=1
#         
#    plt.plot(yvals[1:(bins-1)], rho[1:(bins-1)])
#        
    
    
    #Velocity Profile    
    uxAvg = np.zeros(np.size(yvals))
    uxCount = np.zeros(np.size(yvals))
       
    
    for i in range(0, count):
        ux = uxs[i]
        bin = np.floor((y[i]-ymin)/bindiff)
        bin = int(bin)
        uxAvg[bin-1] = uxAvg[bin-1]+ux
        uxCount[bin-1] = uxCount[bin-1]+1
    
    
    for n in range(0, int(np.size(yvals))):
        if uxCount[n] == 0:
            uxAvg[n] = 0
        else:
            uxAvg[n] = uxAvg[n]/uxCount[n]

    slipVs[filenum][0] = uxAvg[0]
    slipVs[filenum][1] = uxAvg[-1]
    yws[filenum][0] = yvals[0]
    yws[filenum][1] = yvals[-1]
    
    fitparam = np.polyfit(yvals, uxAvg, 2)   
    predUx = np.polyval(fitparam, yvals)
    plt.plot(yvals, uxAvg, 'o')
    plt.plot(yvals, predUx, color='r')
        
    fitparams[filenum, :] = fitparam
    filenum += 1
 
#Plot the velocity Profile here
#plt.ylim(ymin = 0)
#plt.ylim(ymax = 25)
#plt.xlabel('y (nm)')
#plt.ylabel(r"$u_x$ (m/s)")
#plt.savefig('Velocity Profiles Plot.jpg', format='jpg', dpi=800, bbox_inches='tight')
#plt.ylabel(r"$\rho$")
#plt.savefig('DPs.png', bbox_inches = 'tight')
#plt.show()


#Calculate the slip length using EQ(1)
accs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
slipLens = np.zeros(len(slipVs))
for i in range(0, len(slipLens)):
    para = fitparams[i, :]
    strain_rate_yw_L = 2*para[0]*yws[i][0]+para[1]
    strain_rate_yw_H = 2*para[0]*yws[i][1]+para[1]
    slipLens[i] = (slipVs[i][0]/strain_rate_yw_L
            +slipVs[i][1]/strain_rate_yw_H)/2
slerr = [1, 0.5, 0.3, 0.3, 0, 0, 0, 3, 0, 0]
#Literature reference data is here
lit_SLvDF = [0.0985932460631662, 14.900662251655625,
0.19774751418096484, 10.132450331125824,
0.2973388166310832, 11.059602649006628,
0.3958275228266289, 10.264900662251655,
0.49728904924229994, 11.324503311258276,
0.5949845104681192, 11.986754966887418,
0.7010240843128087, 10.264900662251655,
0.799118954745891, 9.47019867549669,
0.895555351525526, 10.39735099337748,
1.003466740347694, 11.721854304635762,
1.1912914800732983, 11.4569536423841,
1.3906874440586756, 12.384105960264897,
1.5976797748006857, 12.516556291390728,
1.8049695091950289, 13.70860927152318,
2.006666609996004, 14.23841059602649,
4.035211740643562, 23.112582781456958,
5.9453425504738915, 53.84105960264901]
lit_ebars = [6, 4, 0.5, 1, 1, 1.5, 0.5, 0.5, 0.3, 
                0, 0, 0, 0, 0, 0, 0, 0.5]
lit_df = lit_SLvDF[0::2]
lit_sl = lit_SLvDF[1::2]

lit_ebars2 = np.array(lit_ebars)
lit_ebars2[lit_ebars>=lit_sl] = lit_sl[lit_ebars>=lit_sl]*.999999
plt.errorbar(lit_df, lit_sl, yerr=[lit_ebars2, lit_ebars], fmt='r^')

plt.errorbar(accs, slipLens, yerr=slerr, fmt='bo')

accs2 = [2, 3, 4]
sl2 = [11.3525, 16.3128, 21.5341]
plt.plot(accs2, sl2,'bo')

plt.ylim(ymin = 0)
plt.ylim(ymax = 60)
plt.xlabel(r"$F_x / 10^{11}\ (m/s^2)$ ")
plt.ylabel(r"$L_s$ (nm)")

plt.xscale('log')
plt.title('Slip Length vs Driving Force')
plt.savefig('SLCompare.jpg',format='jpg', dpi=800, bbox_inches = 'tight')
plt.show()


##Plot the Slip velocity here
#accs = [0.1, 0.2, 0.3, 0.4, 0.5,0.6, 0.7, 0.8, 0.9, 1]
#lit_UXvDF = [0.09810344592846734, 1.8896785524649715,
#0.20394831788043402, 4.023608217947142,
#0.3011776879195087, 6.156720990074742,
#0.40268621764761947, 8.091124453702566,
#0.5020408718975071, 10.025323693991744,
#0.6035684624705578, 12.092472327737607,
#0.7029135862979755, 13.960298982967768,
#0.8044697681384363, 16.22656537189069,
#0.9039197266130241, 18.824490462770076,
#1.005494969298425, 21.223502021811044,
#1.2066059442606436, 26.81779193726258]
#lit_df2 = lit_UXvDF[0::2]
#lit_ux = lit_UXvDF[1::2]
#
#
#plt.plot(accs, slipVs[:,1], 'bo')
#plt.plot(lit_df2, lit_ux, 'r^')
#plt.xlabel(r"$F_x / 10^{11}\ (m/s^2)$ ")
#plt.ylabel(r"$u_s$ (m/s)")
#plt.title('Slip Velocity vs Driving Force')
#plt.savefig('SVcompare.jpg',format='jpg', dpi=800, bbox_inches = 'tight')
#plt.show()
#    
    
    
    
    
 