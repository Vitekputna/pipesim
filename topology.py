import numpy as np


class node:

    def __init__(self) -> None:
        self.inlet_components = []
        self.outlet_components = []
        pass

    def add_inlet_component(self, component_ID : int) -> None:
        self.inlet_components.append(component_ID)

    def add_outlet_component(self, component_ID : int) -> None:
        self.outlet_components.append(component_ID)

class component:
    def __init__(self,inlet_node : int, outlet_node : int) -> None:
        self.type = "base"
        self.inlet_node = inlet_node
        self.outlet_node = outlet_node

    def set_inletOutlet(self,inlet_node : int,outlet_node : int) -> None:
        self.inlet_node = inlet_node
        self.outlet_node = outlet_node

    def get_coeff(self,inlet_pressure : float, outlet_pressure : float, inlet_density : float, outlet_density : float, viscosity : float) -> float:
        return 0

class pipe(component):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node,outlet_node)
        self.type = "pipe"
        self.length = 1
        self.inlet_area = 1
        self.outlet_area = 1

    def get_coeff(self,inlet_pressure : float, outlet_pressure : float, inlet_density : float, outlet_density : float, viscosity : float) -> float:

        area = (self.inlet_area+self.outlet_area)/2

        diameter = np.sqrt(4*area/np.pi)

        density = (inlet_density+outlet_density)/2
        return (np.pi*density*diameter**4)/(128*viscosity*self.length)
        
class general(component):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        super().__init__(inlet_node, outlet_node)
        self.type = "general"
        self.length = 1
        self.inlet_area = 1
        self.outlet_area = 1
        self.inlet_height = 0
        self.outlet_height = 0
        self.resistance_coeff = 1

    def get_coeff(self,inlet_pressure : float, outlet_pressure : float, inlet_density : float, outlet_density : float, viscosity : float) -> float:
        gravity = 9.81
        density = (inlet_density+outlet_density)/2
        area = (self.inlet_area+self.outlet_area)/2

        eps = 1e-6 # Division by zero

        A1 = ((area/self.inlet_area)**2)*density**2
        A2 = ((area/self.outlet_area)**2)*density**2

        K1 = area*density/(np.abs(inlet_pressure-outlet_pressure + eps))

        K2 = np.abs((outlet_pressure-inlet_pressure + gravity*(self.outlet_height*outlet_density-self.inlet_height*inlet_density))/
                    (A1/inlet_density - A2/outlet_density - self.resistance_coeff*A1/inlet_density))

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

class topology:

    def __init__(self) -> None:
        self.components = []
        self.nodes = []
        self.N_nodes = 0
        self.N_components = 0

    def add_component(self, component : component) -> None:
        self.N_components += 1
        self.components.append(component)
        self.add_node_from_component(component)

    def add_node_from_component(self, component : component) -> None:   
        num_nodes_toadd = max(0,component.inlet_node-len(self.nodes)+1)
        num_nodes_toadd = max(num_nodes_toadd,component.outlet_node-len(self.nodes)+1)

        for i in range(num_nodes_toadd):
            self.nodes.append(node())

        self.N_nodes = len(self.nodes)

        component_ID = len(self.components)-1

        self.nodes[component.inlet_node].outlet_components.append(component_ID)
        self.nodes[component.outlet_node].inlet_components.append(component_ID)

    def get_component(self, component_id : int) -> component:
        return self.components[component_id]

    def print(self) -> None:
        print("Components:")
        for component in self.components:
            print(component.type, component.inlet_node, component.outlet_node)

        print("Nodes:")
        for node in self.nodes:
            print(node.inlet_components, node.outlet_components)