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

    inlet_node = None
    outlet_node = None

    type = "base"

    def __init__(self) -> None:
        pass

    def __init__(self,inlet_node : int, outlet_node : int) -> None:
        self.inlet_node = inlet_node
        self.outlet_node = outlet_node

    def set_inletOutlet(self,inlet_node : int,outlet_node : int) -> None:
        self.inlet_node = inlet_node
        self.outlet_node = outlet_node

class pipe(component):
    type = "pipe"

class topology:

    def __init__(self) -> None:
        self.components = []
        self.nodes = []

    def add_component(self, component : component) -> None:
        self.components.append(component)
        self.add_node_from_component(component)

    def add_node_from_component(self, component : component) -> None:
        
        num_nodes_toadd = max(0,component.inlet_node-len(self.nodes)+1)
        num_nodes_toadd = max(num_nodes_toadd,component.outlet_node-len(self.nodes)+1)

        for i in range(num_nodes_toadd):
            self.nodes.append(node())

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

class variables:

    def __init__(self) -> None:
        pass

    def __init__(self, per_node : int, per_component : int) -> None:
        self.values_per_node = per_node
        self.values_per_component = per_component

    def init_variables(self, per_node_size : int, per_component_size : int) -> None:
        self.node_values = np.zeros((self.values_per_node,per_node_size))
        self.component_values = np.zeros((self.values_per_component,per_component_size))


class solver:

    def __init__(self) -> None:
        pass

    def solve(self, variables : variables):
        print("")

class pressure_correction_solver(solver):

    def solve(self, variables : variables):
        print("Incompressible stacionary solver")
        size = len(variables.node_values)
        print(size)
        A = np.zeros((size,size))
        

class pipesim:

    def __init__(self, node_variable_size : list, component_variable_size :list) -> None:
        self.topology = topology()
        self.variables = variables(node_variable_size[0],component_variable_size[0])
        self.variables.init_variables(node_variable_size[1],component_variable_size[1])

    def set_solver(self, solver : solver) -> None:
        self.solver = solver()

    def solve(self) -> None:
        self.solver.solve(self.variables)

    def print_variables(self) -> None:
        print(self.variables.node_values)
        print(self.variables.component_values)

    

    

    


