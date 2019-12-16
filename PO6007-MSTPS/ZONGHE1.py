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
CV1  =  0.009487  # Kong Zhi Fa
CT   =  0.001116  # Wo Lun
CV2  =  0.004016  # Pang Tong Fa

# Qi Fa Mo Kuai
class Valve:
    def __init__(self, Cv=0.01, Yst=0.5):
        self._Cv = Cv
        self._Yst = Yst

    def __str__(self):
        return ("Cv: " + str(self._Cv) + "\n" +
                "Yst: " + str(self._Yst))

    def setYst(self, Yst):
        self._Yst = Tst

    def calcVolFlux(self, rho1=1.177, p1=PATM, p2=PATM):
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


v1 = Valve(Cv=CV1, Yst=0.2)
print(v1)
print(v1.calcVolFlux(p1=2*PATM, p1=PATM))


