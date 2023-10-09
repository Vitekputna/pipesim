from CRSprop import CRSprop

class properties:
    def __init__(self) -> None:
        self.gravity = 9.81
        pass

    def density(self, temperature, pressure) -> float:
        return 0.
    
    def viscosity(self, temperature, pressure) -> float:
        return 0.
    
class constant_properties(properties):
    def __init__(self) -> None:
        super().__init__()
        self.density_value = 0
        self.viscosity_value = 0
        self.temperature = 300

    def set_density(self, value) -> None:
        self.density_value = value

    def set_viscosity(self, value) -> None:
        self.viscosity_value = value

    def set_temperature(self, value : float) -> None:
        self.temperature = value

    def density(self, temperature, pressure) -> float:
        return self.density_value

    def viscosity(self, temperature, pressure) -> float:
        return self.viscosity_value
    
class compresible_isothermal(properties):
    def __init__(self) -> None:
        super().__init__()
        self.compresibility = 1
        self.viscosity_value = 0
        self.temperature = 300

    def set_compresibility(self, value) -> None:
        self.compresibility = value

    def set_viscosity(self, value) -> None:
        self.viscosity_value = value

    def set_temperature(self, value : float) -> None:
        self.temperature = value

    def density(self, temperature, pressure) -> float:
        return self.compresibility*pressure
    
    def viscosity(self, temperature, pressure) -> float:
        return self.viscosity_value
    
class CRSprop_isothermal(properties):
    def __init__(self) -> None:
        super().__init__()
        self.props = CRSprop()
        self.specie = ""
        self.temperature = 300

    def set_specie(self, value : str) -> None:
        self.specie = value
        self.props.add_specie(value)

    def set_temperature(self, value : float) -> None:
        self.temperature = value
    
    def density(self, temperature, pressure) -> float:
        return self.props.density(self.specie,pressure/1e6,temperature)
    
    def viscosity(self, temperature, pressure) -> float:
        return self.props.dynamic_viscosity(self.specie,pressure/1e6,temperature)