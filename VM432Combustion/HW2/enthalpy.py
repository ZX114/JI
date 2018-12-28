"""
Created on Mon Sep 24 10:56:40 2018
C7H16 + 11 O2 = 7 CO2 + 8 H2O
CH4 + 2 O2 = CO2 + 2 H2O
enthalpies of formation
@author: xzhang
"""
import numpy as np

def kcal2kJ(h):
    return h * 4.184

#enthalpies of formation for the 4 species in kJ/mol
dHf0716 = np.array([kcal2kJ(-44.9),0.0,kcal2kJ(-94.0),kcal2kJ(-57.8)])
dHf014 = np.array([kcal2kJ(-17.8),0.0,kcal2kJ(-94.0),kcal2kJ(-57.8)])

#heat of combustion kJ/mol(fuel)
q716 = 8*dHf0716[3] + 7*dHf0716[2] - 11*dHf0716[1] - dHf0716[0]
q14 = 2*dHf014[3] + 1*dHf014[2] - 2*dHf014[1] - dHf014[0]
