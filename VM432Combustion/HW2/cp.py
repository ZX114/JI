"""
Created on Mon Sep 24 11:30:01 2018
heat capacities
@author: xzhang
"""
import csv
import numpy as np

#CO2
filename1 = 'cpCO2.txt'
data1 = []
with open(filename1) as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    data10 = [row for row in reader]
    data1 = np.array(data10,dtype=float)
    data1 = np.transpose(data1)
T1 = data1[0]
cp1 = data1[1]
abcdCO2 = np.polyfit(T1,cp1,3)
def cpCO2(T):
    return (abcdCO2[0]*T**3 + abcdCO2[1]*T**2 + abcdCO2[2]*T**1 + abcdCO2[3])


#H2O
filename1 = 'cpH2O.txt'
data1 = []
with open(filename1) as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    data10 = [row for row in reader]
    data1 = np.array(data10,dtype=float)
    data1 = np.transpose(data1)
T1 = data1[0]
cp1 = data1[1]
abcdH2O= np.polyfit(T1,cp1,3)
def cpH2O(T):
    return (abcdH2O[0]*T**3 + abcdH2O[1]*T**2 + abcdH2O[2]*T**1 + abcdH2O[3])


#O2
filename1 = 'cpO2.txt'
data1 = []
with open(filename1) as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    data10 = [row for row in reader]
    data1 = np.array(data10,dtype=float)
    data1 = np.transpose(data1)
T1 = data1[0]
cp1 = data1[1]
abcdO2= np.polyfit(T1,cp1,3)
def cpO2(T):
    return (abcdO2[0]*T**3 + abcdO2[1]*T**2 + abcdO2[2]*T**1 + abcdO2[3])


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


#CH4
filename1 = 'cpCH4.txt'
data1 = []
with open(filename1) as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    data10 = [row for row in reader]
    data1 = np.array(data10,dtype=float)
    data1 = np.transpose(data1)
T1 = data1[0]
cp1 = data1[1]
abcdCH4= np.polyfit(T1,cp1,3)
def cpCH4(T):
    return (abcdCH4[0]*T**3 + abcdCH4[1]*T**2 + abcdCH4[2]*T**1 + abcdCH4[3])


#C7H16
filename1 = 'cpC7H16.txt'
data1 = []
with open(filename1) as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    data10 = [row for row in reader]
    data1 = np.array(data10,dtype=float)
    data1 = np.transpose(data1)
T1 = data1[0]
cp1 = data1[1]
abcdC7H16= np.polyfit(T1,cp1,3)
def cpC7H16(T):
    return (abcdC7H16[0]*T**3 + abcdC7H16[1]*T**2 + abcdC7H16[2]*T**1 + 
            abcdC7H16[3])
