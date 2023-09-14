class properies:
    
    def __init__(self) -> None:
        pass

    def density(self, temperature, pressure) -> float:
        return 0.
    
    def viscosity(self, temperature, pressure) -> float:
        return 0.
    
class constant_properties(properies):
    def __init__(self) -> None:
        super().__init__()
        self.density = 0
        self.viscosity = 0

    def set_density(self, value):
        self.density = value

    def set_viscosity(self, value):
        self.viscosity = value

    def density(self, temperature, pressure) -> float:
        return self.density

    def viscosity(self, temperature, pressure) -> float:
        return self.viscosity