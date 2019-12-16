# Mon Dec 16 10:42:25 CST 2019
# ZONG HE ZUO YE 1

# Constants
PATM =  101.3e03  # Pa
CP   =  1004.0    # J/kg K
RG   =  287.0     # J/kg K
K    =  1.4       # -
PCR  =  0.528     # -
P0   =  18000e03  # Pa 
H0   =  299.3e03  # J/kg
H1   =  299.3e03  # J/kg
CV1  =  0.009487  # Control Valve
CT   =  0.001116  # Turbine
CV2  =  0.004016  # Bypass Valve


def main():
    v1 = Valve(Cv=CV1, Yst=1)
    t1 = Turbine(Ct=CT)
    cb = Chamber(vol = 0.25)
    print(t1)
    print(v1)
    print(cb)
    print(v1.calcVolFlux(p1=2*PATM, p2=PATM))
    print(t1.calcVolFlux(p1=2*PATM, p2=PATM))
    pass

# Valve module
class Valve:
    def __init__(self, Cv=0.01, Yst=0.5):
        self._Cv = Cv
        self._Yst = Yst

    def __str__(self):
        return ("|VALVE|\n\tCv: " + str(self._Cv) + "\n" +
                "\tYst: " + str(self._Yst))

    def setYst(self, Yst):
        self._Yst = Tst

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

    def updateP(self, G1, G2, G3, h1, h2, dt):
        temp = (G1*h1 - (G2+G3)*h2) / (self._V * (CP/RG - 1.0))
        temp = temp * dt
        self._P = self._P + temp
        self._Rho = self._P / (RG * self._T)

    def updateH(self, G1, G2, G3, h1, h2, dt):
        temp = G1*h1 - (G2+G3)*h2 + (1.0 - RG/CP)*(G2+G3-G1)*h2
        temp = temp / (self._Rho * self._V * (1.0 - RG/CP))
        temp = temp * dt
        self._H = self._H + temp
        self._T = self._H / CP
        self._Rho = self._P / (RG * self._T)

main()

