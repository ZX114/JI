# Mon Dec 16 10:42:25 CST 2019
# ZONG HE ZUO YE 1
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# Configurations
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 16
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['font.style'] = 'normal'
mpl.rcParams['font.serif'] = 'DejaVu Serif'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fallback_to_cm'] = True
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'

# Constants
PATM =  101.3e03       # Pa
CP   =  1004.0         # J/kg K
RG   =  287.0          # J/kg K
K    =  1.4            # -
PCR  =  0.528          # -
P0   =  18000e03       # Pa
P1   =  PATM           # Initial Pressure of the Chamber
P3   =  PATM           # Outlet Pressure
H0   =  299.3e03       # J/kg
H1   =  299.3e03       # J/kg
T0   =  H0 / CP        # K
RHO0 =  P0 / (T0 * RG) # kg/m3
CV1  =  0.009487       # Control Valve
CT   =  0.001116       # Turbine
CV2  =  0.004016       # Bypass Valve
VCB1 =  0.25           # m3
VCB2 =  0.50           # m3


def main():
    controlValv = Valve(Cv=CV1, Yst=0.0)
    bypassValv = Valve(Cv=CV2, Yst=0.0)
    tb = Turbine(Ct=CT)

    dt = 0.001
    time = np.arange(0.0, 10.0+dt, dt)
    p_cb1 = np.zeros(len(time))
    T_cb1 = np.zeros(len(time))
    G2_tb1 = np.zeros(len(time))
    G1_tb1 = np.zeros(len(time))
    G3_tb1 = np.zeros(len(time))
    p_cb2 = np.zeros(len(time))
    T_cb2 = np.zeros(len(time))
    G2_tb2 = np.zeros(len(time))
    G1_tb2 = np.zeros(len(time))
    G3_tb2 = np.zeros(len(time))

    # VCB1
    cb = Chamber(vol=VCB1, p=P1, h=H1)
    for it in range(len(time)):
        t = time[it]
        controlValv.setYst(Yst_Control(t))
        bypassValv.setYst(Yst_Bypass(t))
        G1 = controlValv.calcVolFlux(RHO0, P0, cb.getPressure())
        G2 = tb.calcVolFlux(cb.getRho(), cb.getPressure(), P3)
        G3 = bypassValv.calcVolFlux(cb.getRho(), cb.getPressure(), P3)
        cb.updateState(G1, G2, G3, H0, cb.getEnthalpy(), dt)
        p_cb1[it] = cb.getPressure()
        T_cb1[it] = cb.getEnthalpy()
        G2_tb1[it] = G2
        G1_tb1[it] = G1
        G3_tb1[it] = G3

    # VCB2
    cb = Chamber(vol=VCB2, p=P1, h=H1)
    for it in range(len(time)):
        t = time[it]
        controlValv.setYst(Yst_Control(t))
        bypassValv.setYst(Yst_Bypass(t))
        G1 = controlValv.calcVolFlux(RHO0, P0, cb.getPressure())
        G2 = tb.calcVolFlux(cb.getRho(), cb.getPressure(), P3)
        G3 = bypassValv.calcVolFlux(cb.getRho(), cb.getPressure(), P3)
        cb.updateState(G1, G2, G3, H0, cb.getEnthalpy(), dt)
        p_cb2[it] = cb.getPressure()
        T_cb2[it] = cb.getEnthalpy()
        G2_tb2[it] = G2
        G1_tb2[it] = G1
        G3_tb2[it] = G3




    dt = 0.04
    time2 = np.arange(0.0, 10.0+dt, dt)
    p_cb1_dt2 = np.zeros(len(time2))
    T_cb1_dt2 = np.zeros(len(time2))
    G2_tb1_dt2 = np.zeros(len(time2))
    G1_tb1_dt2 = np.zeros(len(time2))
    G3_tb1_dt2 = np.zeros(len(time2))

    # VCB1
    cb = Chamber(vol=VCB1, p=P1, h=H1)
    for it in range(len(time2)):
        t = time2[it]
        controlValv.setYst(Yst_Control(t))
        bypassValv.setYst(Yst_Bypass(t))
        G1 = controlValv.calcVolFlux(RHO0, P0, cb.getPressure())
        G2 = tb.calcVolFlux(cb.getRho(), cb.getPressure(), P3)
        G3 = bypassValv.calcVolFlux(cb.getRho(), cb.getPressure(), P3)
        cb.updateState(G1, G2, G3, H0, cb.getEnthalpy(), dt)
        p_cb1_dt2[it] = cb.getPressure()
        T_cb1_dt2[it] = cb.getEnthalpy()
        G2_tb1_dt2[it] = G2
        G1_tb1_dt2[it] = G1
        G3_tb1_dt2[it] = G3





    fig = plt.figure(figsize=(7,5))
    ax = plt.subplot(111)
    ax.plot(time, p_cb1, label='dt=0.01')
    ax.plot(time2, p_cb1_dt2, label='dt=0.04')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Pressure (Pa)')
    ax.legend()
    plt.tight_layout()
    plt.show()

    fig = plt.figure(figsize=(7,5))
    ax = plt.subplot(111)
    ax.plot(time, T_cb1, label='dt=0.01')
    ax.plot(time2, T_cb1_dt2, label='dt=0.04')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Enthalpy (kJ/kg)')
    ax.legend()
    plt.tight_layout()
    plt.show()

    fig = plt.figure(figsize=(7,5))
    ax = plt.subplot(111)
    ax.plot(time, G2_tb1, label='dt=0.01')
    ax.plot(time2, G2_tb1_dt2, label='dt=0.04')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('G2 (kg/m3 s)')
    ax.legend()
    plt.tight_layout()
    plt.show()

    fig = plt.figure(figsize=(7,5))
    ax = plt.subplot(111)
    ax.plot(time, G1_tb1, label='dt=0.01')
    ax.plot(time2, G1_tb1_dt2, label='dt=0.04')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('G1 (kg/m3 s)')
    ax.legend()
    plt.tight_layout()
    plt.show()

    fig = plt.figure(figsize=(7,5))
    ax = plt.subplot(111)
    ax.plot(time, G3_tb1, label='dt=0.01')
    ax.plot(time2, G3_tb1_dt2, label='dt=0.04')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('G3 (kg/m3 s)')
    ax.legend()
    plt.tight_layout()
    plt.show()

# Valve module
class Valve:
    def __init__(self, Cv=0.01, Yst=0.5):
        self._Cv = Cv
        self._Yst = Yst

    def __str__(self):
        return ("|VALVE|\n\tCv: " + str(self._Cv) + "\n" +
                "\tYst: " + str(self._Yst))

    def setYst(self, Yst):
        self._Yst = Yst

    def calcVolFlux(self, rho1=1.184, p1=PATM, p2=PATM):
        pRatio = p2 / p1
        kRecip = 1.0 / K
        if pRatio > PCR:
            temp = rho1 * p1 * (pRatio**(2.0*kRecip) - pRatio**(1.0+kRecip))
            temp = temp**0.5
            volFlux = self._Yst * self._Cv * temp
        else:
            temp = rho1 * p1 * (PCR**(2.0*kRecip) - PCR**(1.0+kRecip))
            temp = temp**0.5
            volFlux = self._Yst * self._Cv * temp
        return volFlux


# Turbine module
class Turbine:
    def __init__(self, Ct=CT):
        self._Ct = Ct

    def __str__(self):
        return ("|TURBINE|\n\tCt: " + str(self._Ct))

    def calcVolFlux(self, rho1=1.184, p1=PATM, p2=PATM):
        pRatio = p2 / p1
        if pRatio > PCR:
            temp = rho1 * p1 * (1.0 - pRatio**2)
            temp = temp**0.5
            volFlux = self._Ct * temp
        else:
            temp = rho1 * p1 * (1.0 - PCR**2)
            temp = temp**0.5
            volFlux = self._Ct * temp
        return volFlux


# Chamber module
class Chamber:
    def __init__(self, vol=0.25, p=PATM, h=H1):
        self._V = vol
        self._P = p
        self._H = h
        self._T = h / CP
        self._Rho = p / (RG * self._T)

    def __str__(self):
        return ("|CHAMBER|\n\tVolume: " + str(self._V) + "\n" +
                "\tPressure: " + str(self._P) + "\n" +
                "\tEnthalpy: " + str(self._H) + "\n" +
                "\tTemperature: " + str(self._T) + "\n" +
                "\tDensity: " + str(self._Rho))

    def updateState(self, G1, G2, G3, h1, h2, dt):
        # update pressure
        temp = (G1*h1 - (G2+G3)*h2) / (self._V * (CP/RG - 1.0))
        temp = temp * dt
        self._P = self._P + temp
        # update enthalpy
        temp = G1*h1 - (G2+G3)*h2 + (1.0 - RG/CP)*(G2+G3-G1)*h2
        temp = temp / (self._Rho * self._V * (1.0 - RG/CP))
        temp = temp * dt
        self._H = self._H + temp
        self._T = self._H / CP
        self._Rho = self._P / (RG * self._T)

    def getPressure(self):
        return self._P

    def getRho(self):
        return self._Rho

    def getEnthalpy(self):
        return self._H

    def getTemperature(self):
        return self._T

def Yst_Control(t):
    if t < 1.0:
        ret = t
    else:
        ret = 1.0
    return ret

def Yst_Bypass(t):
    if t < 6.0:
        ret = 0.0
    elif t < 7.0:
        ret = t - 6.0
    else:
        ret = 1.0
    return ret

main()
