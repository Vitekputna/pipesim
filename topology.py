from properties import properties

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

    # def get_coeff(self,inlet_pressure : float, outlet_pressure : float, inlet_density : float, outlet_density : float, viscosity : float) -> float:
    def get_coeff(self, inlet_node_values : list, outlet_node_values : list, component_values : list, properties : properties) -> float:
        return 0

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