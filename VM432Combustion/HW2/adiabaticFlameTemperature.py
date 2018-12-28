"""
Created on Mon Sep 24 13:34:29 2018
C7H16 + 11 O2 = 7 CO2 + 8 H2O
CH4 + 2 O2 = CO2 + 2 H2O
adiabatic flame temperature
@author: xzhang
"""
import numpy as np
from sympy import integrate
from sympy.abc import x
import enthalpy as en
import cp

r = [1., 11., 7., 8.]
W = 100.0 #molecular weight of fuel
cpFuel = cp.cpC7H16 #choose cp of specific fuel
q0 = en.q716 #heat of combustion
filename = 'TadC7H16.txt'

cpN2 = cp.cpN2
cpCO2 = cp.cpCO2
cpH2O = cp.cpH2O
cpO2 = cp.cpO2
q = -q0*1000.0 #heat of combustion J/mol(fuel)

T0 = 298.15 #initial temperature
Z0 = np.arange(0.001,1.001,0.001)
Tad = []

#|heat of combustion| minus enthalpy increase
def qD(Z,T1):
    #q =  hN2(T,T0) + hCO2(T,T0) + hH2O(T,T0) + {hFuel(T,T0) + hO2(T,T0)}
    nAir = W*(1.0-Z)/((32.0+3.76*28.0)*Z) #n mol O2 per mol fuel
    if nAir >= r[1]:
        hN2 = 3.76 * nAir * integrate(cpN2(x),(x,T0,T1))
        hCO2 = r[2] * integrate(cpCO2(x),(x,T0,T1))
        hH2O = r[3] * integrate(cpH2O(x),(x,T0,T1))
        hO2 = (nAir-r[1]) * integrate(cpO2(x),(x,T0,T1))
        hFuel = 0.0
        qr = q
    if nAir < r[1]:
        hN2 = 3.76 * nAir * integrate(cpN2(x),(x,T0,T1))
        hCO2 = r[2]/r[1] * nAir * integrate(cpCO2(x),(x,T0,T1))
        hH2O = r[3]/r[1] * nAir * integrate(cpH2O(x),(x,T0,T1))
        hFuel = (1.0 - nAir/r[1]) *integrate(cpFuel(x),(x,T0,T1))
        hO2 = 0.0
        qr = q * (nAir/r[1])
    qDiff = qr - (hN2+hCO2+hH2O+hO2+hFuel)
    return qDiff

#bisection method to solve Tad
for Z in Z0:
    a = 298.0
    b = 2700.0
    fa = qD(Z,a)
    fb = qD(Z,b)
    epsilon = 0.002
    k = 0
    while abs(b - a)/2.0 > epsilon:
        x1 = (a+b)/2.0
        fx1 = qD(Z,x1)
        if fx1*fa < 0.0:
            b = x1
            fb = fx1
        else:
            a = x1
            fa = fx1
        k = k+1
    
    xStar = (a+b)/2.0
    print xStar,k
    Tad.append(xStar)


with open(filename, 'w+') as writer:
    for i in range(0,len(Tad)):
        line1 = str('%.3f' %Z0[i])
        writer.write(line1)
        writer.write('\t')
        line2 = str('%.3f' %Tad[i])
        writer.write(line2)
        writer.write('\n')
