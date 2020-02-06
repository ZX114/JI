# Sat Dec 21 19:09:07 CST 2019
# ZONG HE ZUO YE 2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
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
P0   =  150000.0       # Pa
P1   =  140000.0       # Initial Pressure of the Chamber
P3   =  PATM           # Outlet Pressure
T0   =  373.0          # K
T1   =  T0             # Initial Temperature of the Chamber
H0   =  T0 * CP        # J/kg
H1   =  H0             # J/kg
RHO0 =  P0 / (T0 * RG) # kg/m3
RHO1 =  P1 / (T1 * RG) # kg/m3
CVA  =  5.158e-7       # VA
CV1  =  4.1452e-8      # VA1
CV2  =  6.356e-7       # VA2
CV3  =  1.325e-8       # VA3
VCB1 =  0.02           # m3
VCB2 =  0.04           # m3
LV   =  351.0          # kJ/kg


def func(x):
    VA = Valve(CVA, 0.5)
    VA.setYst(0.95)
    # return VA.calcVolFlux(RHO1, P1, x) - 0.001e-3
    return VA.calcVolFlux(RHO0, P0, x) - 0.05e-3


def main():
    X = fsolve(func, [130000.0])
    print(X)





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

    def updateState(self, G1, G2, G3, G4, G5, h1, h2, h3, dt):
        # update pressure
        temp = (G1*h1 + G2*h2 - (G3+G4+G5)*h3) / (self._V * (CP/RG - 1.0))
        temp = temp * dt
        self._P = self._P + temp
        # update enthalpy
        temp = G1*h1 + G2*h2 - (G3+G4+G5)*h3 + (1.0 - RG/CP)*(G3+G4+G5-G1-G2)*h3
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
