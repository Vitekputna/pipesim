import numpy as np

class discharge_model:
    def __init__(self, length : float = 1.0, diameter : float = 1.0) -> None:
        self.length = length
        self.diameter = diameter

    def check_validity(self) -> None:
        pass

    def discharge_coeff(self, Re : float) -> float:
        return 0.0

class linear_model(discharge_model):
    #source: Atomization and Sprays Arthur H. Lefebvre and Vincent G. McDonell page:108 eq:5.9

    def __init__(self, length: float, diameter: float) -> None:
        super().__init__(length, diameter)

    def check_validity(self) -> None:

        ratio = self.length/self.diameter

        if ratio > 2 and ratio < 10:
            print("Discharge model is in valid range")
        else:
            print("Discharge model is outside valid range")
        
    def discharge_coeff(self, Re : float) -> float:
        return 0.827-0.0085*self.length/self.diameter
    
class Nakayama(discharge_model):
    #source: Atomization and Sprays Arthur H. Lefebvre and Vincent G. McDonell page:110 eq:5.12 and eq:5.13

    def __init__(self, length: float, diameter: float) -> None:
        super().__init__(length, diameter)

    def check_validity(self) -> None:

        ratio = self.length/self.diameter

        if ratio > 1.5 and ratio < 17:
            print("Discharge model is in valid range")
        else:
            print("Discharge model is outside valid range")

    def discharge_coeff(self, Re: float) -> float:
        ratio = self.length/self.diameter

        if Re > 550 and Re < 7000:
            return (Re**(5/6))/(17.11*ratio + 1.65*Re**0.8)
        else:
            return 0.868 - 0.0425*np.sqrt(ratio)
        
class Lichtarowicz(discharge_model):
    #source: Atomization and Sprays Arthur H. Lefebvre and Vincent G. McDonell page:110 eq:5.15

    def __init__(self, length: float, diameter: float) -> None:
        super().__init__(length, diameter)

    def check_validity(self) -> None:

        ratio = self.length/self.diameter

        if ratio > 2 and ratio < 10:
            print("Discharge model is in valid range")
        else:
            print("Discharge model is outside valid range")

    def discharge_coeff(self, Re: float) -> float:
        #valid for 10 < Re < 20000
        ratio = self.length/self.diameter
        Cd_max = 0.827-0.0085*ratio

        return 1/(1/Cd_max + 20*(1+2.25*ratio)/Re)

        
