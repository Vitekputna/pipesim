import numpy as np
from variables import variables
from topology import topology
from conditions import condition

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
        