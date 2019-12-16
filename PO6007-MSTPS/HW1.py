# Sun Oct 27 15:40:29 2019
# Constant volume chamber
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
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'

###################### thermophysical prop ##################
Rg = 0.28698  # kJ/kg K
cv = 0.740  # kJ/kg K
cp = Rg + cv  # kJ/kg K
#T = np.arange(270, 410, 10)
#h = [270.11, 280.13, 290.16, 300.19, 310.24, 320.29, 330.34, 340.42,
#     350.49, 360.67, 370.67, 380.77, 390.28, 400.98]
#u = [192.60, 199.75, 206.91, 214.07, 221.25, 228.43, 235.61, 242.82,
#     250.02, 257.24, 264.46, 271.69, 278.93, 286.16]
def energy(ti):
    return 192.60 + cv * (ti - 270)
    
def enthalpy(ti):
    return 270.11 + cp * (ti - 270)

def rho(ti):
    return 1.1614 - 0.002903*(ti - 300)

###################### constants ############################
patm = 101325.0
hconv = 100  # W/m2
# cube
l1 = 0.5  # m
vol = l1**3
AG = 6 * l1**2
# tube
ri = 0.05
ro1 = 0.04
ro2 = 0.04
Ai = np.pi * ri**2
Ao1 = np.pi * ro1**2
Ao2 = np.pi * ro2**2
Tinf = 300  # K

##################### initial conditions ######################
pG0 = patm
TG0 = Tinf

##################### input ###################################
t = np.arange(0, 61, 0.001)  # sec
Tin = 400  # K
pin = patm + 0.01 * patm * np.sin(t) + 0.1 * patm
po1 = patm
po2 = patm
zetai = 5.7
zetao1 = 5.7
zetao2 = 5.7

###################### output ##################################
pG = np.zeros(len(t))
TG = np.zeros(len(t))
Mi_t = np.zeros(len(t))
Mo1_t = np.zeros(len(t))
Mo2_t = np.zeros(len(t))

################################# main #########################
pG[0] = pG0
TG[0] = TG0
def valve(p1, p2, zeta, tem, area):
    temp = 2*p1*p2*(p2 - p1)/(Rg * tem *(p2 - p1 - zeta*p2))
    return area * np.sqrt(temp)
Mi_t[0] = valve(pin[0], pG[0], zetai, Tin, Ai)
Mo1_t[0] = valve(pG[0], po1, zetao1, TG[0], Ao1)
Mo1_t[0] = valve(pG[0], po2, zetao2, TG[0], Ao2)
for it in range(len(t)-1):
    time = t[it+1]
    dt = t[it+1] - t[it]
    Mi = valve(pin[it], pG[it], zetai, Tin, Ai)
    Mo1 = valve(pG[it], po1, zetao1, TG[it], Ao1)
    Mo2 = valve(pG[it], po2, zetao2, TG[it], Ao2)
    Mi_t[it+1] = Mi
    Mo1_t[it+1] = Mo1
    Mo2_t[it+1] = Mo2
    # TG
    rhs = Mi*enthalpy(Tin) - Mo1*enthalpy(TG[it]) - Mo2*enthalpy(TG[it]) + \
          hconv*AG*(Tinf - TG[it])
    rhs -= energy(TG[it]) * (Mi - Mo1 - Mo2)
    dTem = dt * rhs / ( rho(TG[it] * vol * cv) )
    TG[it+1] = TG[it] + dTem
    gradT = ( TG[it+1] - TG[it] ) / dt
    # pG
    rhs = Rg * TG[it+1] / vol * ( Mi - Mo1 - Mo2) + rho(TG[it+1]) * Rg * gradT
    dpres = rhs * dt
    pG[it+1] = pG[it] + dpres

fig = plt.figure(figsize = (16, 6))
ax1 = plt.subplot(131)
ax1.plot(t, pG)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Pressure (Pa)')
ax2 = plt.subplot(132)
ax2.plot(t, TG)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Temperature (K)')
ax3=plt.subplot(133)
mass = rho(TG) * vol
ax3.plot(t, mass)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Mass (kg)')
fig.suptitle('$p_{in} = 1.1p_{atm} + 0.01p_{atm}sin(t)$')
plt.tight_layout()
plt.show()


fig = plt.figure(figsize = (16, 6))
ax1 = plt.subplot(131)
ax1.plot(t, Mi_t)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel(r'$\dot{m}_{VA}$ (kg/s)')
ax2 = plt.subplot(132)
ax2.plot(t, Mo1_t)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel(r'$\dot{m}_{VA1}$ (kg/s)')
ax3=plt.subplot(133)
mass = rho(TG) * vol
ax3.plot(t, Mo2_t)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel(r'$\dot{m}_{VA2}$ (kg/s)')
fig.suptitle('$p_{in} = 1.1p_{atm} + 0.01p_{atm}sin(t)$')
plt.tight_layout()
plt.show()

