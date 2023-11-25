from CRSprop import CRSprop
from variables import variables

class properties:
    def __init__(self) -> None:
        self.gravity = 9.81
        pass

    def update_temperature(self,variables : variables) -> None:
        pass

    def density(self, temperature, pressure) -> float:
        return 0.
    
    def viscosity(self, temperature, pressure) -> float:
        return 0.
    
class constant_properties(properties):
    def __init__(self) -> None:
        super().__init__()
        print("Setting constant properties model")
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
        print("Setting compressible isothermal model")
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
        print("Setting CRSprop isothermal model")
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
    
    def enthalpy(self,temperature,pressure) -> float:
        return self.props.enthalpy(self.specie,pressure/1e6,temperature)
    
    def entropy(self,temperature,pressure) -> float:
        return self.props.entropy(self.specie,pressure/1e6,temperature)
    
    def liquid_density(self,temperature) -> float:
        return self.props.liquid_density(self.specie,temperature)
    
    def vapor_density(self,temperature) -> float:
        return self.props.vapor_density(self.specie,temperature)
    
    def liquid_enthalpy(self,temperature) -> float:
        return self.props.liquid_enthalpy(self.specie,temperature)
    
    def vapor_enthalpy(self,temperature) -> float:
        return self.props.vapor_enthalpy(self.specie,temperature)
    
    def liquid_entropy(self,temperature) -> float:
        return self.props.liquid_entropy(self.specie,temperature)
    
    def vapor_entropy(self,temperature) -> float:
        return self.props.vapor_entropy(self.specie,temperature)
    
    def vapor_pressure(self,temperature) -> float:
        return self.props.saturated_pressure(self.specie,temperature)
    
    def vapor_temperature(self,pressure) -> float:
        return self.props.saturated_temperature(self.specie,pressure)
    
class CRSprop_equilibrium(properties):
    def __init__(self) -> None:
        super().__init__()
        print("Setting CRSprop isothermal model")
        self.props = CRSprop()
        self.specie = ""
        self.pressure_idx = 0
        self.temperature_idx = 1

    def set_specie(self, value : str) -> None:
        self.specie = value
        self.props.add_specie(value)
    
    def update_temperature(self,variables : variables) -> None:

        for node_val in variables.node_values:
            pressure = node_val[self.pressure_idx]
            temperature = node_val[self.temperature_idx]

            if pressure <= self.vapor_pressure(temperature):
                node_val[self.temperature_idx] = self.vapor_temperature(pressure)

    def density(self, temperature, pressure) -> float:
        return self.props.density(self.specie,pressure/1e6,temperature)
    
    def viscosity(self, temperature, pressure) -> float:
        return self.props.dynamic_viscosity(self.specie,pressure/1e6,temperature)
    
    def enthalpy(self,temperature,pressure) -> float:
        return self.props.enthalpy(self.specie,pressure/1e6,temperature)
    
    def entropy(self,temperature,pressure) -> float:
        return self.props.entropy(self.specie,pressure/1e6,temperature)
    
    def liquid_density(self,temperature) -> float:
        return self.props.liquid_density(self.specie,temperature)
    
    def vapor_density(self,temperature) -> float:
        return self.props.vapor_density(self.specie,temperature)
    
    def liquid_enthalpy(self,temperature) -> float:
        return self.props.liquid_enthalpy(self.specie,temperature)
    
    def vapor_enthalpy(self,temperature) -> float:
        return self.props.vapor_enthalpy(self.specie,temperature)
    
    def liquid_entropy(self,temperature) -> float:
        return self.props.liquid_entropy(self.specie,temperature)
    
    def vapor_entropy(self,temperature) -> float:
        return self.props.vapor_entropy(self.specie,temperature)
    
    def vapor_pressure(self,temperature) -> float:
        return self.props.saturated_pressure(self.specie,temperature)
    
    def vapor_temperature(self,pressure) -> float:
        return self.props.saturated_temperature(self.specie,pressure)