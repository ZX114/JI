# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 11:17:18 2018
Rankine solids
@author: xzhang
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

U = 1.0
Q = 1.0
lRange = np.array([0.1,1.0,10.0])
#psi(r,theta)=0.5*U*r**2*(sin(theta))** \
#   2-Q/(4*pi)*(cos(theta1)-cos(theta2))
#===============================================#
#plt.figure(figsize=(8,5))
for i,l in enumerate(lRange):
    l = lRange[i]
    colorDict = {0:'r',1:'b',2:'g'}
    labelDict = {0:'l=%.1f' %(lRange[0]), \
                 1:'l=%.1f' %(lRange[1]), \
                 2:'l=%.1f' %(lRange[2])}
    thetaRange = np.linspace(0.0001, \
                             2*np.pi-0.0001,1000)
    rRange = np.array([])
    
    for theta in thetaRange:
        def psi(r):
            cos1 = (r*np.cos(theta)+l)/ \
                (l**2+2.0*l*r* \
                 np.cos(theta)+r**2)**0.5
            cos2 = (r*np.cos(theta)-l)/ \
                (l**2-2.0*l*r* \
                 np.cos(theta)+r**2)**0.5
            return 0.5*U*r**2*(np.sin(theta))**2 \
                    -Q/(4*np.pi)*(cos1-cos2)
        ri = fsolve(psi,[0.5])
        rRange = np.append(rRange,ri)
    
    x = rRange*np.cos(thetaRange)
    y = rRange*np.sin(thetaRange)
    plt.plot(x,y,c=colorDict[i], \
             label=labelDict[i])
plt.axis([-12,12,-0.7,0.7])
plt.xlabel('x')
plt.ylabel('y')
plt.legend(bbox_to_anchor=(1.08,0.1))
plt.savefig('RkSolids.eps')
plt.show()
