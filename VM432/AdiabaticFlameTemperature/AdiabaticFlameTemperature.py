# Mon Sep 24 13:34:29 2018
# =============================================================================
# Adiabatic Flame Temperature of nHeptane and Methane with 1-step chemistry
# C7H16 + 11 O2 = 7 CO2 + 8 H2O
# =============================================================================

import csv
import numpy as np
from sympy import integrate
from sympy.abc import x
import matplotlib.pyplot as plt


def kcal2kJ(h):
    return h * 4.184

# Fit cp data
def fitCp(specie):
    filename1 = f'cp{specie}'
    data1 = []
    with open(filename1) as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        data10 = [row for row in reader]
        data1 = np.array(data10, dtype=float)
        data1 = np.transpose(data1)
    T1 = data1[0]
    cp1 = data1[1]
    abcd = np.polyfit(T1,cp1,3)
    return abcd
coeffs = {'C7H16':[], 'O2':[], 'N2':[], 'CO2':[], 'H2O':[]}
for specie in ['C7H16','O2','N2','CO2','H2O']:
    coeffs[specie] = fitCp(specie)
def cp(specie, T):
    c = coeffs[specie]
    return (c[0]*T**3 + c[1]*T**2 + c[2]*T**1 + c[3])

# |heat of combustion| minus enthalpy increase
T0 = 298.15 #initial temperature
W = 100.0  # molecular weight of fuel
def qD(Z, T1, qc):
    if Z <= 0.0:
        Z = 1e-10
    nAir = W*(1.0-Z)/((32.0+3.76*28.0)*Z)  # n mol O2 per mol fuel
    if nAir >= r[1]:
        hN2 = 3.76 * nAir * integrate(cp('N2', x), (x,T0,T1))
        hCO2 = r[2] * integrate(cp('CO2', x), (x,T0,T1))
        hH2O = r[3] * integrate(cp('H2O', x), (x,T0,T1))
        hO2 = (nAir-r[1]) * integrate(cp('O2', x), (x,T0,T1))
        hFuel = 0.0
        qr = qc
    else:
        hN2 = 3.76 * nAir * integrate(cp('N2', x), (x,T0,T1))
        hCO2 = r[2]/r[1] * nAir * integrate(cp('CO2', x), (x,T0,T1))
        hH2O = r[3]/r[1] * nAir * integrate(cp('H2O', x), (x,T0,T1))
        hFuel = (1.0 - nAir/r[1]) *integrate(cp('C7H16', x), (x,T0,T1))
        hO2 = 0.0
        qr = qc * (nAir/r[1])
    qDiff = qr - (hN2+hCO2+hH2O+hO2+hFuel)
    return qDiff


# enthalpies of formation for the 4 species in kJ/mol
dHfa = np.array([kcal2kJ(-44.9), 0.0, kcal2kJ(-94.0), kcal2kJ(-57.8)])
qc = -1000.0*(8*dHfa[3] + 7*dHfa[2] - 11*dHfa[1] - dHfa[0])  # [J/mol]
r = [1., 11., 7., 8.]  # reaction order
filename = 'TadC7H16.csv'
Z0 = np.arange(0,1.01,0.01)
Tad = []


# Bisection method to solve Tad
for Z in Z0:
    a = 298.0
    b = 3000.0
    fa = qD(Z, a, qc)
    fb = qD(Z, b, qc)
    epsilon = 0.01
    k = 0
    while abs(b - a)/2.0 > epsilon:
        x1 = (a+b)/2.0
        fx1 = qD(Z, x1, qc)
        if fx1*fa < 0.0:
            b = x1
            fb = fx1
        else:
            a = x1
            fa = fx1
        k = k+1    
    xStar = (a+b)/2.0
    print(xStar, k)
    Tad.append(xStar)

# Plot
ax = plt.subplot(111)
ax.plot(Z0, Tad)
ax.set_xlabel(r'$Z$ (-)')
ax.set_ylabel(r'$T_{ad}$ (K)')
ax.set_title('Adiabatic Flame Temperature of C7H16')
plt.show()

# Output
with open(filename, 'w+') as writer:
    for i in range(0, len(Tad)):
        writer.write(f'{Z0[i]},{Tad[i]}\n')
