from topology import component
from properties import properties
from friction_factor import *
from loss_models import *
from discharge_models import discharge_model
import numpy as np
    
class general(component):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node, outlet_node)
        self.type = "general"

        self.length = 1
        self.area = 1
        self.inlet_area = 1
        self.outlet_area = 1
        self.inlet_height = 0
        self.outlet_height = 0

        self.resistance_coeff = 1

    def set_diameter(self, diameter : float) -> None:
        self.area = np.pi*(diameter**2)/4
        self.inlet_area = self.area
        self.outlet_area = self.area

    def set_inlet_diameter(self, diameter : float) -> None:
        area = np.pi*(diameter**2)/4
        self.inlet_area = area
        self.area = (self.inlet_area+self.outlet_area)/2

    def set_outlet_diameter(self, diameter : float) -> None:
        area = np.pi*(diameter**2)/4
        self.outlet_area = area
        self.area = (self.inlet_area+self.outlet_area)/2

    def diameter(self) -> float:
        self.area = (self.inlet_area+self.outlet_area)/2
        return np.sqrt(4*self.area/np.pi)
    
    def get_resistance_coeff(self, Re : float) -> float:
        return self.resistance_coeff

    def get_coeff(self, inlet_node_values : list, outlet_node_values : list, component_values : list, properties : properties) -> float:
        gravity = properties.gravity

        inlet_pressure = inlet_node_values[0]
        outlet_pressure = outlet_node_values[0]

        inlet_density = properties.density(properties.temperature,inlet_pressure)
        outlet_density = properties.density(properties.temperature,outlet_pressure)

        viscosity = properties.viscosity(properties.temperature,(inlet_pressure+outlet_pressure)/2)

        density = (inlet_density+outlet_density)/2
        area = (self.inlet_area+self.outlet_area)/2
        velocity = component_values[0]

        eps = 1e-6 # Division by zero

        Re = density*self.diameter()*velocity/viscosity

        resistance_coeff = self.get_resistance_coeff(Re)

        A1 = ((area/self.inlet_area)**2)*density**2
        A2 = ((area/self.outlet_area)**2)*density**2

        K1 = area*density/(np.abs(inlet_pressure-outlet_pressure + eps))

        K2 = np.abs((outlet_pressure-inlet_pressure + gravity*(self.outlet_height*outlet_density-self.inlet_height*inlet_density))/
                    (A1/inlet_density - A2/outlet_density - resistance_coeff*A1/inlet_density))

        return K1*np.sqrt(2*K2)
    
    def bernouli_residual(self, massflow : float, inlet_pressure : float, outlet_pressure : float, inlet_density : float, outlet_density : float) -> float:

        gravity = 9.81
        density = (inlet_density+outlet_density)/2
        area = (self.inlet_area+self.outlet_area)/2

        velocity = massflow/(area*density)

        inlet_velocity = area*density/(self.inlet_area*inlet_density)*velocity
        outlet_velocity = area*density/(self.outlet_area*outlet_density)*velocity

        inlet = inlet_pressure+gravity*inlet_density*self.inlet_height + 0.5*inlet_density*inlet_velocity**2
        outlet = outlet_pressure + gravity*outlet_density*self.outlet_height + 0.5*outlet_density*outlet_velocity**2 + 0.5*self.resistance_coeff*inlet_density*inlet_velocity**2

        return inlet-outlet
        
class pipe(general):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node, outlet_node)
        self.type = "pipe"

        self.critical_Re = 2300
        self.smoothing_interval = 1000
        self.roughness = 1e-3

    def get_lambda(self, Re : float) -> float:
        # Laminar flow
        if Re < self.critical_Re:
            return laminar(Re)
        elif Re >= self.critical_Re and Re < self.critical_Re + self.smoothing_interval:
            phi = (self.critical_Re+self.smoothing_interval-Re)/self.smoothing_interval

            return phi*laminar(Re) + (1-phi)*Churchill(Re,self.roughness,self.diameter())
        else:
            return Churchill(Re,self.roughness,self.diameter())
        
    def get_resistance_coeff(self, Re : float) -> float:
        return self.get_lambda(abs(Re))*self.length/self.diameter()
        
class area_change(general):

    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node, outlet_node)

        self.type = "contraction"
        self.length = 1
        self.area = 1
        self.inlet_area = 1
        self.outlet_area = 1
        self.inlet_height = 0
        self.outlet_height = 0
        
        self.orientation = 1 # 1 for inlet smaller than outlet

    def set_diameter(self, diameter: float) -> None:
        print("Method not supported for this component, use set_diameters()")

    def set_diameters(self, inlet_diameter: float, outlet_diameter : float) -> None:
        self.inlet_area = np.pi*(inlet_diameter**2)/4
        self.outlet_area = np.pi*(outlet_diameter**2)/4

        if self.inlet_area > self.outlet_area:
            self.orientation = -1

    def compute_contraction_loss(self, Re : float) -> float:
        if Re*self.orientation > 0:
            return sudden_expansion(self.inlet_area,self.outlet_area)
        else:
            return sudden_contraction(self.inlet_area,self.outlet_area)

    def get_resistance_coeff(self, Re : float) -> float:
        return self.compute_contraction_loss(Re)

class orifice(general):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node, outlet_node)
        self.type = "orifice"
        self.length = 1
        self.area = 1

        self.model = discharge_model()

    def set_discharge_model(self,model : discharge_model) -> None:
        self.model = model

    def get_discharge_coeff(self, Re : float) -> float:
        return self.model.discharge_coeff(Re)

    def get_coeff(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:
        inlet_pressure = inlet_node_values[0]
        outlet_pressure = outlet_node_values[0]

        inlet_density = properties.density(properties.temperature,inlet_pressure)
        outlet_density = properties.density(properties.temperature,outlet_pressure)

        density = (inlet_density+outlet_density)/2
        area = (self.inlet_area+self.outlet_area)/2

        viscosity = properties.viscosity(properties.temperature,(inlet_pressure+outlet_pressure)/2)
        velocity = component_values[0]

        Re = density*self.diameter()*velocity/viscosity

        discharge_coeff = self.get_discharge_coeff(Re)

        return discharge_coeff*area*np.sqrt((2*density)/(abs(outlet_pressure-inlet_pressure)))
    
class Kv_valve(general):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node, outlet_node)
        self.type = "valve"
        self.length = 1
        
        self.Kv = 1e-8 #in SI units m^3/sPa

    def get_coeff(self, inlet_node_values: list, outlet_node_values: list, component_values: list, properties: properties) -> float:

        inlet_pressure = inlet_node_values[0]
        outlet_pressure = outlet_node_values[0]

        inlet_density = properties.density(properties.temperature,inlet_pressure)
        outlet_density = properties.density(properties.temperature,outlet_pressure)

        density = (inlet_density+outlet_density)/2

        return  density*self.Kv