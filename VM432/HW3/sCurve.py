# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:09:33 2018

the S-curve

@author: xzhang
"""
from math import e
import numpy as np
import matplotlib.pyplot as plt
#==============================================================================#
T0 = np.arange(0.1,0.30,0.05)
Ta = 1.0
Tf = np.arange(0.001,2,0.001)
#==============================================================================#
plt.rcParams["font.sans-serif"] = ["Times New Roman"]
plt.rcParams['axes.unicode_minus'] = False
labelfontsize = 30
legendfontsize = 26
ticksfontsize = 30
plt.figure(figsize=(12,8))


for iT0 in T0:
    xDa = np.array([])
    yTf = np.array([])
    labelT0 = r'$\tilde{T}_0 = %.2f$' %iT0
    for iTf in Tf:
        Da = (iTf-iT0)/((1.0+iT0-iTf)*(e**(-Ta/iTf)))
        if Da<0.0 or Da>120.0:
            continue
        else:
            xDa = np.append(xDa, Da)
            yTf = np.append(yTf, iTf)
    plt.plot(xDa,yTf,label=labelT0,linewidth=20.0*iT0)
plt.legend(loc='right',ncol=2,fontsize=legendfontsize)
plt.xlim(0.0,50.0)
plt.ylim(0.0,1.5)

my_x_ticks = np.arange(0.0, 120.0, 20.0)
my_y_ticks = np.arange(0.0, 2.0, 0.5)
plt.xticks(my_x_ticks,color='k')
plt.yticks(my_y_ticks,color='k')
plt.tick_params(labelsize=ticksfontsize)
plt.xlabel('$Da$',fontsize=labelfontsize,color='k')
plt.ylabel(r'$\tilde{T}_f$',fontsize=labelfontsize,color='k')

plt.savefig('sCurve.eps') 
plt.show()

            
