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

    def set_density(self, value):
        self.density_value = value

    def set_viscosity(self, value):
        self.viscosity_value = value

    def density(self, temperature, pressure) -> float:
        return self.density_value

    def viscosity(self, temperature, pressure) -> float:
        return self.viscosity_value