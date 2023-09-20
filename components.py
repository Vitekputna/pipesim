from topology import component
from properties import properties
from friction_factor import *
import numpy as np

class laminar_pipe(component):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node,outlet_node)
        self.type = "laminar_pipe"
        self.length = 1
        self.area = 1
        self.inlet_area = 1
        self.outlet_area = 1

    def set_diameter(self, diameter : float) -> None:
        self.area = np.pi*(diameter**2)/4
        self.inlet_area = self.area
        self.outlet_area = self.area

    def diameter(self) -> float:
        return np.sqrt(4*self.area/np.pi)

    # def get_coeff(self,inlet_pressure : float, outlet_pressure : float, inlet_density : float, outlet_density : float, viscosity : float) -> float:
    def get_coeff(self, inlet_node_values : list, outlet_node_values : list, component_values : list, properties : properties) -> float:

        inlet_pressure = inlet_node_values[0]
        outlet_pressure = outlet_node_values[0]

        inlet_density = properties.density(300,inlet_pressure)
        outlet_density = properties.density(300,outlet_pressure)

        viscosity = properties.viscosity(300,(inlet_pressure+outlet_pressure)/2)

        diameter = np.sqrt(4*self.area/np.pi)
        density = (inlet_density+outlet_density)/2
        return (np.pi*density*diameter**4)/(128*viscosity*self.length)
    
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

    def diameter(self) -> float:
        self.area = (self.inlet_area+self.outlet_area)/2
        return np.sqrt(4*self.area/np.pi)
    
    def get_resistance_coeff(self, Re : float) -> float:
        return self.resistance_coeff

    def get_coeff(self, inlet_node_values : list, outlet_node_values : list, component_values : list, properties : properties) -> float:
        gravity = properties.gravity

        inlet_pressure = inlet_node_values[0]
        outlet_pressure = outlet_node_values[0]

        inlet_density = properties.density(300,inlet_pressure)
        outlet_density = properties.density(300,outlet_pressure)

        viscosity = properties.viscosity(300,(inlet_pressure+outlet_pressure)/2)

        density = (inlet_density+outlet_density)/2
        area = (self.inlet_area+self.outlet_area)/2
        velocity = component_values[0]

        eps = 1e-6 # Division by zero

        Re = self.diameter()*velocity/viscosity

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
        self.roughness = 1e-3

    def get_lambda(self, Re : float) -> float:
        return 1
        # Laminar flow
        if Re < self.critical_Re:
            return laminar(Re)
        else:
            return Churchill(Re,self.roughness,self.diameter())
        
    def get_resistance_coeff(self, Re : float) -> float:
        return self.get_lambda(Re)*self.length/self.diameter()
        # return 1
        

        
    
