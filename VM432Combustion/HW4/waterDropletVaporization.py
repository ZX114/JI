# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 10:25:14 2018
water droplet vaporization
@author: xzhang
"""
import numpy as np
import matplotlib.pyplot as plt

Tinf=372.0
Yinf=0.0
ql = 540.0*4.184*1000.0 #J/kg
cp = 0.3*4.184*1000.0 #J/kg K
Wair = 29.0e-3 #kg/mol
Wwater = 18.0e-3 #kg/mol
#==============================================================================#
#mass fraction from psat
def Y(Tem):
    Tem = float(Tem)
    p = 101325.0*np.exp((ql*Wwater/8.314)*(1.0/373.15 - 1.0/Tem))
    X = p/101325.0
    Y = X*Wwater/(X*Wwater+(1.0-X)*Wair)
    if Y>1.0 or Y<0.0:
        Y=0.1
    return Y

def eqT(Y):
    a = (Y-Yinf)/(1.0-Yinf)
    b = ql*a
    c = b/cp
    T = Tinf - c
    return T

#iteration with a relaxation fractor of 0.1
T0 = Tinf
iterN=50
T = np.linspace(0.0,1.0,iterN)
for i in range(iterN):
    T[i] = T0
    Yi = Y(T0)
    Ti = eqT(Yi)
    T0 = 0.9*T0 + 0.1*Ti
    
Bhv = cp*(Tinf-T0)/ql
mTilde = np.log(1.0+Bhv)
print mTilde    

plt.plot(range(iterN),T,label='T',c='k',linewidth=2)
plt.axis([0, iterN, 200, 400])
plt.xlabel('iterations')
plt.ylabel('T (K)')
plt.legend()
plt.savefig('dropletTIter.eps')
plt.show()
