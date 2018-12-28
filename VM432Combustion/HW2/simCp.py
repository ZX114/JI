# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 10:18:21 2018

adiabatic flame temperature

simplified cp

@author: xzhang
"""

import csv
import numpy as np
def cpCH4(T):
    t = T-273.15
    return 1000.0*(0.034 + 2.5e-6*t)

def cpO2(T):
    t = T-273.15
    return 1000.0*(0.03 + 3.0e-6*t)

def cpCO2(T):
    t = T-273.15
    return 1000.0*(0.04 + 9.7e-6*t)

def cpH2O(T):
    t = T-273.15
    return 1000.0*(0.033 + 5.5e-6*t)

#N2
filename1 = 'cpN2.txt'
data1 = []
with open(filename1) as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    data10 = [row for row in reader]
    data1 = np.array(data10,dtype=float)
    data1 = np.transpose(data1)
T1 = data1[0]
cp1 = data1[1]
abcdN2= np.polyfit(T1,cp1,3)
def cpN2(T):
    return (abcdN2[0]*T**3 + abcdN2[1]*T**2 + abcdN2[2]*T**1 + abcdN2[3])
