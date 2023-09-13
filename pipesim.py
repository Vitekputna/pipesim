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

class pipe(component):
    def __init__(self, inlet_node: int, outlet_node: int) -> None:
        self.type = "pipe"
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

class condition:
    def __init__(self, index : int) -> None:
        self.index = index
        self.index_in_vector = 0
        self.value = 0
        self.type = "base"

class set_pressure(condition):
    def __init__(self, node_idx: int, pressure : float) -> None:
        super().__init__(node_idx)
        self.type = "node"
        self.value = pressure

class properies:
    
    def __init__(self) -> None:
        pass

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
    
    def find_boundary(self, index : int, boundary_conditions : list) -> condition:
        
        for cond in boundary_conditions:
            if cond.index == index:
                return cond
            
        return None
    
    def apply_boundary_conditions(self, variables : variables, boundary_conditions : list) -> None:

        for cond in boundary_conditions:
            if cond.type == "node":
                variables.node_values[cond.index_in_vector][cond.index] = cond.value

            if cond.type == "component":
                variables.node_values[cond.index_in_vector][cond.index] = cond.value


class pressure_correction_solver(solver):

    def solve(self, variables : variables, topology : topology, boundary_condition : list) -> None:
        print("Incompressible stacionary solver")
        
        self.apply_boundary_conditions(variables,boundary_condition)

        nodes_to_solve = self.get_nodes(topology,boundary_condition)
            
        size = len(nodes_to_solve)

        A = np.zeros((size,size))
        b = np.zeros(size)

        for node in nodes_to_solve:

            inlet_components = topology.nodes[node].inlet_components
            outlet_components = topology.nodes[node].outlet_components

            row = nodes_to_solve.index(node)
            
            for inlet_component in inlet_components:

                inlet_node = topology.components[inlet_component].inlet_node
                outlet_node = topology.components[inlet_component].outlet_node
                
                if inlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(inlet_node)

                    A[row][col] -= 1
                else:
                    boundary_value = variables.node_values[0][inlet_node]
                    b[row] += boundary_value

                if outlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(outlet_node)

                    A[row][col] += 1
                else:
                    boundary_value = variables.node_values[0][outlet_node]
                    b[row] -= boundary_value

            for outlet_component in outlet_components:

                inlet_node = topology.components[outlet_component].inlet_node
                outlet_node = topology.components[outlet_component].outlet_node
                
                if inlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(inlet_node)

                    A[row][col] += 1
                else:
                    boundary_value = variables.node_values[0][inlet_node]
                    b[row] -= boundary_value

                if outlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(outlet_node)

                    A[row][col] -= 1
                else:
                    boundary_value = variables.node_values[0][outlet_node]
                    b[row] += boundary_value

        # print(A)
        # print(b)

        result = np.linalg.solve(A,b)

        for i in range(size):
            variables.node_values[0][nodes_to_solve[i]] = result[i]
        

        
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

    

    

    


