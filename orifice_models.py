import numpy as np
from properties import properties
from discharge_models import discharge_model

class mass_flow_model:
    def __init__(self, length : float, diameter : float, discharge_model : discharge_model) -> None:

        self.diameter = diameter
        self.length = length

        self.area = np.pi*(diameter**2)/4

        self.Cd_model = discharge_model(length,diameter)

    def mass_flux(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:
        return 0.0
    
class incompressible_model(mass_flow_model):
    def __init__(self, length: float, diameter: float, discharge_model: discharge_model) -> None:
        super().__init__(length, diameter, discharge_model)

    def mass_flux(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:
        inlet_pressure = inlet_node_values[0]
        outlet_pressure = outlet_node_values[0]

        inlet_density = properties.density(properties.temperature,inlet_pressure)
        outlet_density = properties.density(properties.temperature,outlet_pressure)

        density = (inlet_density+outlet_density)/2
        viscosity = properties.viscosity(properties.temperature,(inlet_pressure+outlet_pressure)/2)
        velocity = component_values[0]

        Re = density*self.diameter()*velocity/viscosity

        Cd = self.Cd_model.discharge_coeff(Re)

        return Cd*self.area*np.sqrt((2*density)/(abs(outlet_pressure-inlet_pressure)))
    
class HEM_model(mass_flow_model):
    def __init__(self) -> None:
        super().__init__()
        self.process = "isoentropic"

    def mass_flux_isoentropic(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:
        return 0.0
    
    def mass_flux_adiabatic(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:
        return 0.0

    def mass_flux(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:
        
        if self.process == "isoentropic":
            return self.mass_flux_isoentropic(self,inlet_node_values,outlet_node_values,component_values,properties)
        elif self.process == "adiabatic":
            return self.mass_flux_adiabatic(self,inlet_node_values,outlet_node_values,component_values,properties)
        else:
            print("Unknown orifice model")
            return 0.0
    

class NHNE(mass_flow_model):
    def __init__(self) -> None:
        super().__init__()

    def mass_flux(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:
        return super().mass_flux(inlet_node_values, outlet_node_values, component_values, properties)
    
