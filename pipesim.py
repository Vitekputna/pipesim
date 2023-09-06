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

    def __init__(self,inlet_node : int, outlet_node : int) -> None:
        self.inlet_node = inlet_node
        self.outlet_node = outlet_node

    def set_inletOutlet(self,inlet_node : int,outlet_node : int) -> None:
        self.inlet_node = inlet_node
        self.outlet_node = outlet_node

class pipe(component):
    type = "pipe"

    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        self.length = 0
        self.diameter = 0
        super().__init__(inlet_node,outlet_node)

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

class variables:

    def __init__(self) -> None:
        self.values_per_node = 0
        self.values_per_component = 0

    def init_variables(self, N_nodes : int, N_components : int) -> None:
        self.node_values = np.zeros((self.values_per_node,N_nodes))
        self.component_values = np.zeros((self.values_per_component,N_components))

class solver:

    def __init__(self) -> None:
        pass

    def solve(self, variables : variables, topology : topology, boundary_condition : list) -> bool:
        return True
    
    def get_nodes(self, topology : topology, boundary_condition : list) -> list:
        nodes_to_solve = []
        found = False
        for i in range(topology.N_nodes):
            for boundary in boundary_condition:
                if boundary.index == i:
                    found = True

            if found == True:
                found = False
                continue

            nodes_to_solve.append(i)

        return nodes_to_solve

class pressure_correction_solver(solver):

    def solve(self, variables : variables, topology : topology, boundary_condition : list) -> bool:
        print("Incompressible stacionary solver")
        
        nodes_to_solve = self.get_nodes(topology,boundary_condition)

        print(nodes_to_solve)
            
        size = len(nodes_to_solve)

        A = np.zeros((size,size))

        for i in range(size):
            print(topology.nodes[nodes_to_solve[i]].inlet_components)
            print(topology.nodes[nodes_to_solve[i]].inlet_components)


        print(A)

class condition:
    def __init__(self, index : int) -> None:
        self.index = index

class set_pressure(condition):
    def __init__(self, node_idx: int, pressure : float) -> None:
        type = "node"
        self.pressure = pressure
        super().__init__(node_idx)
        
class pipesim:

    def __init__(self) -> None:
        self.topology = topology()
        self.variables = variables()
        self.boundary_conditions = []

    def set_solver(self, solver : solver) -> None:
        self.solver = solver()

    def add_component(self, component : component) -> None:
        self.topology.add_component(component)

        self.variables.values_per_component = 1
        self.variables.values_per_node = 1
        self.variables.init_variables(self.topology.N_nodes,self.topology.N_components)

    def add_boundary_condition(self,boundary_condition : condition) -> None:
        self.boundary_conditions.append(boundary_condition)

    def solve(self) -> None:
        self.solver.solve(self.variables,self.topology,self.boundary_conditions)

    def print_variables(self) -> None:
        print(self.variables.node_values)
        print(self.variables.component_values)

    

    

    


