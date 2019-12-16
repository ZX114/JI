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
cv = 4183.0  # kJ/kg K
rho = 995.0  # kg/m3
kappa = 0.682  # W/m K
###################### constants ############################
Tin = 200  # degree
u = 5.0  # m/s
N = 50
L = 50.0  # m
d = L/N
x = np.arange(d/2, L+d/2, d)  # cell center

##################### input ###################################
dt = 0.0001
t = np.arange(10, 50.0001, dt)  # sec
T = np.zeros(N)
for i in range(len(T)):
    T[i] = 150.0  # K

T_prev = T.copy()

TX = []
#TX.append(T.copy())
idx = [0, 10000, 20000, 50000, 100000, 400000]

###################### output ##################################
Tout = np.zeros(len(t))

################################# main #########################
for it in range(len(t)):
    temp = rho*u*cv*Tin - rho*u*cv*T_prev[0] - \
           kappa * (T_prev[0] - T_prev[1])/d
    T[0] = dt * temp / (rho*d*cv) + T_prev[0]
    
    for ix in range(1,len(T)-1):
        temp = rho*u*cv*(T_prev[ix-1] -T_prev[ix]) + \
               kappa * (T_prev[ix-1] + T_prev[ix+1] - 2.0*T_prev[ix]) / d
        T[ix] = dt * temp / (rho * d *cv) + T_prev[ix]
    
    temp = rho*u*cv*(T_prev[-2] - T_prev[-1]) + \
           kappa * (T_prev[-2] - T_prev[-1]) / d
    
    T[-1] = dt * temp / (rho* d * cv) + T_prev[-1]
    Tout[it] = T[-1]
    for i in range(len(T)):
        T_prev[i] = T[i]
    
    if it in idx:
        TX.append(T.copy())

fig = plt.figure(figsize=(10,6))
ax = plt.subplot(111)
for i in range(len(TX)):
    ax.plot(x, TX[i], label='{:.0f} s'.format(t[idx[i]]))
ax.set_xlim(0,50)
ax.set_xlabel('$x$ (m)')
ax.set_ylabel(u'$T$ (\u2103)')
ax.legend(loc='lower right')
plt.tight_layout()
plt.show()

data = []
data.append(list(t))
data.append(list(Tout))
data = np.array(data)
data = np.transpose(data)
with open(f'Tout-N{N}.csv', 'w+') as f:
    np.savetxt(f, data, delimiter=',')

