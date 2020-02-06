# Sun Oct 27 15:40:29 2019
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# Configurations
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 20
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['font.style'] = 'normal'
mpl.rcParams['font.serif'] = 'DejaVu Serif'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fallback_to_cm'] = True
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'

###################### thermophysical prop ##################
cL = 4183.0
cS = 700.0
rhoL = 994.0  # kg/m3
rhoS = 7850.0 # kg/m3
h = 12000.0 # W/m2 K
kappaL = 0.682
kappaS = 1.3
###################### constants ############################
TH0 = 45
TC0 = 10
Ri = 0.05  # inner radius
Rs = 0.06
Ro = 0.08  # outer radius
pi = np.pi
Ac = pi * Ri**2
As = pi * Rs**2 - Ac
Ah = pi * Ro**2 - pi * Rs**2
L = 6.0  # length
S1 = L * pi * 2 * Rs
S2 = L * pi * 2 * Ri
uh = 0.3
uc = 0.3
Qh = uh * Ah
Qc = uc * Ac

dt = 0.01
t = np.arange(0, 200+dt, dt)
Th2 = np.zeros(len(t))
Tc2 = np.zeros(len(t))
Th2[0] = TH0
Tc2[0] = TC0

nx = 50
dx = L / nx
x = np.arange(dx/2, L+dx/2, dx)
TH = np.zeros(nx)
TS = np.zeros(nx)
TC = np.zeros(nx)
TH[:] = TH0
TS[:] = 0.5 * (TH0 + TC0)
TC[:] = TC0

TH_prev = TH.copy()
TS_prev = TS.copy()
TC_prev = TC.copy()

Th1 = np.zeros(len(t))
Tc1 = np.zeros(len(t))
Th1[:] = TH0
Tc1[:] = TC0
idx = int(100/dt)
Th1[idx::] = TH0 + 10
Tc1[idx::] = TC0

Si1 = S1 / nx
Si2 = S2 / nx


for it in range(len(t)-1):
    rhs = Qh * cL * rhoL * (Th1[it] - TH_prev[0]) - h * Si1 * (TH_prev[0] - TS_prev[0])
    rhs = rhs - kappaL * Ah  * (TH_prev[0] - TH_prev[1]) / dx
    temp = rhs * dt / (cL * rhoL * Ah * dx)
    TH[0] = TH_prev[0] + temp
    
    rhs = h * Si1 * (TH_prev[0] - TS_prev[0]) - h * Si2 * (TS_prev[0] - TC_prev[-1])
    rhs = rhs - kappaS * As * (TS_prev[0] - TS_prev[1]) / dx
    temp = rhs * dt / (cS * rhoS * As * dx)
    TS[0] = TS_prev[0] + temp
    
    rhs = Qc * cL * rhoL * (Tc1[it] - TC_prev[0]) + h * Si2 * (TS_prev[-1] - TC_prev[0])
    rhs = rhs - kappaL * Ac * (TC_prev[0] - TC_prev[1]) / dx
    temp = rhs * dt / (cL * rhoL * Ac * dx)
    TC[0] = TC_prev[0] + temp
    
    for ix in range(1,nx-1):
        rhs = Qh * cL * rhoL * (TH_prev[ix-1] - TH_prev[ix]) - h * Si1 * (TH_prev[ix] - TS_prev[ix])
        rhs = rhs + kappaL * Ah * (TH_prev[ix-1] - TH_prev[ix]) / dx - kappaL * Ah * (TH_prev[ix] - TH_prev[ix+1]) / dx
        temp = rhs * dt / (cL * rhoL * Ah * dx)
        TH[ix] = TH_prev[ix] + temp
        
        rhs = h * Si1 * (TH_prev[ix] - TS_prev[ix]) - h * Si2 * (TS_prev[ix] - TC_prev[nx-ix-1])
        rhs = rhs + kappaS * As * (TS_prev[ix-1] - TS_prev[ix]) / dx - kappaS * As * (TS_prev[ix] - TS_prev[ix+1]) / dx
        temp = rhs * dt / (cS * rhoS * As * dx)
        TS[ix] = TS_prev[ix] + temp
        
        rhs = Qc * cL * rhoL * (TC_prev[ix-1] - TC_prev[ix]) + h * Si2 * (TS_prev[nx-ix-1] - TC[ix])
        rhs = rhs + kappaL * Ac * (TC_prev[ix-1] - TC_prev[ix]) / dx - kappaL * Ac * (TC_prev[ix] - TC_prev[ix+1]) / dx
        temp = rhs * dt / (cL * rhoL * Ac * dx)        
        TC[ix] = TC_prev[ix] + temp
    
    
    rhs = Qh * cL * rhoL * (TH_prev[-2] - TH_prev[-1]) - h * Si1 * (TH_prev[-1] - TS_prev[-1])
    rhs = rhs + kappaL * Ah * (TH_prev[-2] - TH_prev[-1]) / dx
    temp = rhs * dt / (cL * rhoL * Ah * dx)
    TH[-1] = TH_prev[-1] + temp
    
    rhs = h * Si1 * (TH_prev[-1] - TS_prev[-1]) - h * Si2 * (TS_prev[-1] - TC_prev[0])
    rhs = rhs + kappaS * As * (TS_prev[-2] - TS_prev[-1]) / dx
    temp = rhs * dt / (cS * rhoS * As * dx)
    TS[-1] = TS_prev[-1] + temp
    
    rhs = Qc * cL * rhoL * (TC_prev[-2] - TC_prev[-1]) + h * Si2 * (TS_prev[0] - TC_prev[-1])
    rhs = rhs + kappaL * Ac * (TC_prev[-2] - TC_prev[-1]) / dx
    temp = rhs * dt / (cL * rhoL * Ac * dx)
    TC[-1] = TC_prev[-1] + temp
    
    for j in range(0,nx):
        TH_prev[j] = TH[j]
        TS_prev[j] = TS[j]
        TC_prev[j] = TC[j]
    
    Th2[it+1] = TH[-1]
    Tc2[it+1] = TC[-1]


fig = plt.figure(figsize = (10,7))
ax = plt.subplot(111)
ax.plot(t, Th1, label = 'Hot in')
ax.plot(t, Tc1, label = 'Cold in')
ax.plot(t, Th2, label = 'Hot out')
ax.plot(t, Tc2, label = 'Cold out')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature (K)')
ax.legend(loc=0)
plt.show()

fig = plt.figure(figsize = (10,7))
ax = plt.subplot(111)
ax.plot(x, TH, label = 'Hot')
ax.plot(x, TS, label = 'Surface')
ax.plot(x, TC[::-1], label='Cold')
#ax.set_xlim(0,6)
ax.set_xlabel('X (m)')
ax.set_ylabel('Temperature (K)')
ax.legend(loc=0)
plt.show()
