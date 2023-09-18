import numpy as np
from variables import variables
from topology import topology
from conditions import condition
from properties import properties

class solver:

    def __init__(self) -> None:
         self.residual = []

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


    def compute_residual(self, properties : properties, variables : variables, topology : topology, boundary_condition : list) -> float:
        
        nodes_to_solve = self.get_nodes(topology,boundary_condition)

        density = properties.density(300,101325)
        viscosity = properties.viscosity(300,101325)

        total_mass_flow_residual = 0

        for node in nodes_to_solve:

            mass_flow = 0

            inlet_components = topology.nodes[node].inlet_components
            outlet_components = topology.nodes[node].outlet_components

            for inlet_component in inlet_components:

                inlet_node = topology.components[inlet_component].inlet_node
                outlet_node = topology.components[inlet_component].outlet_node

                C = topology.components[inlet_component].get_coeff(variables.node_values[0][inlet_node],variables.node_values[0][outlet_node],density,density,viscosity)

                outlet_pressure = variables.node_values[0][outlet_node]
                inlet_pressure = variables.node_values[0][inlet_node]

                mass_flow += C*(outlet_pressure-inlet_pressure)

            for outlet_component in outlet_components:

                inlet_node = topology.components[outlet_component].inlet_node
                outlet_node = topology.components[outlet_component].outlet_node

                C = topology.components[outlet_component].get_coeff(variables.node_values[0][inlet_node],variables.node_values[0][outlet_node],density,density,viscosity)

                outlet_pressure = variables.node_values[0][outlet_node]
                inlet_pressure = variables.node_values[0][inlet_node]

                mass_flow -= C*(outlet_pressure-inlet_pressure)


            total_mass_flow_residual += mass_flow

        return np.abs(total_mass_flow_residual)
    
    def solve_velocity(self, properties : properties, variables : variables, topology : topology, boundary_condition : list) -> None:

        i = 0
        for component in topology.components:

            inlet_node = component.inlet_node
            outlet_node = component.outlet_node

            outlet_pressure = variables.node_values[0][outlet_node]
            inlet_pressure = variables.node_values[0][inlet_node]

            outlet_density = properties.density(300,outlet_pressure)
            inlet_density = properties.density(300,inlet_pressure)

            viscosity = properties.viscosity(300,inlet_pressure)

            C = component.get_coeff(inlet_pressure,outlet_pressure,inlet_density,outlet_density,viscosity)

            mass_flux = -C*(outlet_pressure-inlet_pressure)

            area = (component.inlet_area + component.outlet_area)/2
            density = (inlet_density+outlet_density)/2

            velocity = mass_flux/(area*density)

            variables.component_values[0][i] = velocity

            i += 1

class laminar_pipe_solver(solver):

    def __init__(self) -> None:
        super().__init__()

    def solve(self, properties : properties, variables : variables, topology : topology, boundary_condition : list) -> None:
        print("Laminar pipe system solver")
        
        self.apply_boundary_conditions(variables,boundary_condition)

        nodes_to_solve = self.get_nodes(topology,boundary_condition)

        size = len(nodes_to_solve)

        A = np.zeros((size,size))
        b = np.zeros(size)

        # TESTING ONLY
        density = 1000
        viscosity = 1e-5

        for node in nodes_to_solve:

            inlet_components = topology.nodes[node].inlet_components
            outlet_components = topology.nodes[node].outlet_components

            row = nodes_to_solve.index(node)
            
            for inlet_component in inlet_components:

                inlet_node = topology.components[inlet_component].inlet_node
                outlet_node = topology.components[inlet_component].outlet_node

                C = topology.components[inlet_component].get_coeff(variables.node_values[0][inlet_node],variables.node_values[0][outlet_node],density,density,viscosity)
                
                if inlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(inlet_node)

                    A[row][col] -= C
                else:
                    boundary_value = variables.node_values[0][inlet_node]
                    b[row] += boundary_value*C

                if outlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(outlet_node)

                    A[row][col] += C
                else:
                    boundary_value = variables.node_values[0][outlet_node]
                    b[row] -= boundary_value*C

            for outlet_component in outlet_components:

                inlet_node = topology.components[outlet_component].inlet_node
                outlet_node = topology.components[outlet_component].outlet_node

                C = topology.components[outlet_component].get_coeff(variables.node_values[0][inlet_node],variables.node_values[0][outlet_node],density,density,viscosity)
                
                if inlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(inlet_node)

                    A[row][col] += C
                else:
                    boundary_value = variables.node_values[0][inlet_node]
                    b[row] -= boundary_value*C

                if outlet_node in nodes_to_solve:
                    col = nodes_to_solve.index(outlet_node)

                    A[row][col] -= C
                else:
                    boundary_value = variables.node_values[0][outlet_node]
                    b[row] += boundary_value*C

        # print(A)
        # print(b)

        result = np.linalg.solve(A,b)

        for i in range(size):
            variables.node_values[0][nodes_to_solve[i]] = result[i]

        self.residual.append(self.compute_residual(properties,variables,topology,boundary_condition))
        self.solve_velocity(properties,variables,topology,boundary_condition)
 
class pressure_correction_solver(solver):

    def __init__(self) -> None:
        super().__init__()
        self.max_iterations = 500
        self.relaxation_factor = 0.9

    def solve(self, properties : properties, variables : variables, topology : topology, boundary_condition : list) -> None:
        print("Pressure correction solver")
        
        self.apply_boundary_conditions(variables,boundary_condition)

        nodes_to_solve = self.get_nodes(topology,boundary_condition)

        size = len(nodes_to_solve)

        # TESTING ONLY

        for i in range(self.max_iterations):

            A = np.zeros((size,size))
            b = np.zeros(size)

            for node in nodes_to_solve:

                inlet_components = topology.nodes[node].inlet_components
                outlet_components = topology.nodes[node].outlet_components

                row = nodes_to_solve.index(node)
                
                for inlet_component in inlet_components:
                    
                    inlet_node = topology.components[inlet_component].inlet_node
                    outlet_node = topology.components[inlet_component].outlet_node

                    outlet_pressure = variables.node_values[0][outlet_node]
                    inlet_pressure = variables.node_values[0][inlet_node]

                    outlet_density = properties.density(300,outlet_pressure)
                    inlet_density = properties.density(300,inlet_pressure)

                    viscosity = properties.viscosity(300,inlet_pressure)

                    C = topology.components[inlet_component].get_coeff(inlet_pressure,outlet_pressure,inlet_density,outlet_density,viscosity)
                    
                    if inlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(inlet_node)

                        A[row][col] -= C
                        b[row] += C*variables.node_values[0][inlet_node]
                    else:
                        boundary_value = variables.node_values[0][inlet_node]
                        b[row] += boundary_value*C

                    if outlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(outlet_node)

                        A[row][col] += C
                        b[row] -= C*variables.node_values[0][outlet_node]
                    else:
                        boundary_value = variables.node_values[0][outlet_node]
                        b[row] -= boundary_value*C

                for outlet_component in outlet_components:

                    inlet_node = topology.components[outlet_component].inlet_node
                    outlet_node = topology.components[outlet_component].outlet_node

                    outlet_pressure = variables.node_values[0][outlet_node]
                    inlet_pressure = variables.node_values[0][inlet_node]

                    outlet_density = properties.density(300,outlet_pressure)
                    inlet_density = properties.density(300,inlet_pressure)

                    viscosity = properties.viscosity(300,inlet_pressure)

                    C = topology.components[outlet_component].get_coeff(inlet_pressure,outlet_pressure,inlet_density,outlet_density,viscosity)
                    
                    if inlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(inlet_node)

                        A[row][col] += C
                        b[row] -= C*variables.node_values[0][inlet_node]
                    else:
                        boundary_value = variables.node_values[0][inlet_node]
                        b[row] -= boundary_value*C

                    if outlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(outlet_node)

                        A[row][col] -= C
                        b[row] += C*variables.node_values[0][outlet_node]
                    else:
                        boundary_value = variables.node_values[0][outlet_node]
                        b[row] += boundary_value*C

            result = np.linalg.solve(A,b)

            for i in range(size):
                variables.node_values[0][nodes_to_solve[i]] += self.relaxation_factor*result[i]

            self.residual.append(self.compute_residual(properties,variables,topology,boundary_condition))

            self.solve_velocity(properties,variables,topology,boundary_condition)