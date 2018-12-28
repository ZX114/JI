# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 12:36:23 2018

python_matplotlib

@author: xzhang
"""



# ====================File Reader====================
import numpy as np
import csv

filename1 = 'TadCH4.txt'
data1 = []
try:
    with open(filename1) as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        data10 = [row for row in reader]
        data1 = np.array(data10,dtype=float)
        data1 = np.transpose(data1)
except csv.Error as e:
    print "Error reading CSV file at lines %s: %s" % (reader.line_num, e)
    sys.exit(-1)
x1 = data1[0]
y1 = data1[1]

filename1 = 'TadC7H16.txt'
data1 = []
try:
    with open(filename1) as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        data10 = [row for row in reader]
        data1 = np.array(data10,dtype=float)
        data1 = np.transpose(data1)
except csv.Error as e:
    print "Error reading CSV file at lines %s: %s" % (reader.line_num, e)
    sys.exit(-1)
x2 = data1[0]
y2 = data1[1]

# ===================================================



# ====================Basic Settings====================
import matplotlib.pyplot as plt
#plt.style.use('ggplot')
plt.rcParams["font.sans-serif"] = ["Times New Roman"]
plt.rcParams['axes.unicode_minus'] = False
labelfontsize = 28
legendfontsize = 30
ticksfontsize = 28
plt.figure(figsize=(14,9))
#plt.grid(True, axis = 'y', color='k',ls='--',linewidth=0.6)
# ======================================================



# ====================Plot Data====================
plt.plot(x1,y1,ls='-',c='k',label='CH4',linewidth = 3)
plt.plot(x2,y2,ls='--',c='k',label='C7H16',linewidth = 3)
# =================================================



# ====================Process====================
plt.legend(loc='upper right',ncol=1,fontsize=legendfontsize)

plt.xlim(0.0,1.0)
plt.ylim(0,2500.0)

my_x_ticks = np.arange(0.0, 1.1, 0.1)
my_y_ticks = np.arange(0.0, 3000.0, 500.0)
plt.xticks(my_x_ticks,color='k')
plt.yticks(my_y_ticks,color='k')
plt.tick_params(labelsize=ticksfontsize)

plt.xlabel('Mixture Fraction',fontsize=labelfontsize,color='k')
plt.ylabel('Adiabatic Flame Temperature (K)',fontsize=labelfontsize,color='k')

plt.savefig('aft.eps') 
plt.show()
# ===============================================
