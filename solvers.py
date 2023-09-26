import numpy as np
from variables import variables
from topology import topology
from conditions import condition
from properties import properties

class solver:

    def __init__(self) -> None:
         self.residual = []
    
         self.pressure_idx = 0
         self.velocity_idx = 0

    def solve(self, variables : variables, topology : topology, boundary_condition : list) -> None:
        pass
    
    def get_nodes(self, topology : topology, boundary_condition : list) -> list:
        nodes_to_solve = []
        found = False

        for index in topology.nodes: 
            for boundary in boundary_condition:
                if boundary.index == index:
                    found = True    

            if found == True:
                found = False
                continue

            nodes_to_solve.append(index)


        # for i in range(topology.N_nodes):
        #     for boundary in boundary_condition:
        #         if boundary.index == i:
        #             found = True

        #     if found == True:
        #         found = False
        #         continue

        #     nodes_to_solve.append(i)

        return nodes_to_solve
    
    def find_boundary(self, index : int, boundary_conditions : list) -> condition:
        
        for cond in boundary_conditions:
            if cond.index == index:
                return cond
            
        return None
    
    def apply_boundary_conditions(self, variables : variables, boundary_conditions : list) -> None:

        for cond in boundary_conditions:
            if cond.type == "node":
                variables.node_values[cond.index][cond.index_in_vector] = cond.value

            if cond.type == "component":
                variables.node_values[cond.index][cond.index_in_vector] = cond.value


    def compute_residual(self, properties : properties, variables : variables, topology : topology, boundary_condition : list) -> float:
        
        nodes_to_solve = self.get_nodes(topology,boundary_condition)

        density = properties.density(properties.temperature,101325)
        viscosity = properties.viscosity(properties.temperature,101325)

        total_mass_flow_residual = 0

        for node in nodes_to_solve:

            mass_flow = 0

            inlet_components = topology.nodes[node].inlet_components
            outlet_components = topology.nodes[node].outlet_components

            for inlet_component in inlet_components:

                inlet_node = topology.components[inlet_component].inlet_node
                outlet_node = topology.components[inlet_component].outlet_node

                C = topology.components[inlet_component].get_coeff(variables.node_values[inlet_node],variables.node_values[outlet_node],variables.component_values[inlet_component],properties)

                outlet_pressure = variables.node_values[outlet_node][self.pressure_idx]
                inlet_pressure = variables.node_values[inlet_node][self.pressure_idx]

                mass_flow += C*(outlet_pressure-inlet_pressure)

            for outlet_component in outlet_components:

                inlet_node = topology.components[outlet_component].inlet_node
                outlet_node = topology.components[outlet_component].outlet_node

                C = topology.components[outlet_component].get_coeff(variables.node_values[inlet_node],variables.node_values[outlet_node],variables.component_values[outlet_component],properties)

                outlet_pressure = variables.node_values[outlet_node][self.pressure_idx]
                inlet_pressure = variables.node_values[inlet_node][self.pressure_idx]

                mass_flow -= C*(outlet_pressure-inlet_pressure)


            total_mass_flow_residual += mass_flow

        return np.abs(total_mass_flow_residual)
    
    def solve_velocity(self, properties : properties, variables : variables, topology : topology, boundary_condition : list) -> None:

        i = 0
        for component in topology.components:

            inlet_node = component.inlet_node
            outlet_node = component.outlet_node

            outlet_pressure = variables.node_values[outlet_node][self.pressure_idx]
            inlet_pressure = variables.node_values[inlet_node][self.pressure_idx]

            outlet_density = properties.density(properties.temperature,outlet_pressure)
            inlet_density = properties.density(properties.temperature,inlet_pressure)

            C = topology.components[i].get_coeff(variables.node_values[inlet_node],variables.node_values[outlet_node],variables.component_values[i],properties)

            mass_flux = -C*(outlet_pressure-inlet_pressure)

            area = (component.inlet_area + component.outlet_area)/2
            density = (inlet_density+outlet_density)/2

            velocity = mass_flux/(area*density)

            variables.component_values[i][self.velocity_idx] = velocity

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

                C = topology.components[inlet_component].get_coeff(variables.node_values[inlet_node],variables.node_values[outlet_node],variables.component_values[inlet_component],properties)
                
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

                C = topology.components[outlet_component].get_coeff(variables.node_values[inlet_node],variables.node_values[outlet_node],variables.component_values[outlet_component],properties)
                
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
        
        print(nodes_to_solve)

        size = len(nodes_to_solve)

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

                    C = topology.components[inlet_component].get_coeff(variables.node_values[inlet_node],variables.node_values[outlet_node],variables.component_values[inlet_component],properties)
                    
                    if inlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(inlet_node)

                        A[row][col] -= C
                        b[row] += C*variables.node_values[inlet_node][self.pressure_idx]
                    else:
                        boundary_value = variables.node_values[inlet_node][self.pressure_idx]
                        b[row] += boundary_value*C

                    if outlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(outlet_node)

                        A[row][col] += C
                        b[row] -= C*variables.node_values[outlet_node][self.pressure_idx]
                    else:
                        boundary_value = variables.node_values[outlet_node][self.pressure_idx]
                        b[row] -= boundary_value*C

                for outlet_component in outlet_components:

                    inlet_node = topology.components[outlet_component].inlet_node
                    outlet_node = topology.components[outlet_component].outlet_node

                    C = topology.components[outlet_component].get_coeff(variables.node_values[inlet_node],variables.node_values[outlet_node],variables.component_values[outlet_component],properties)

                    if inlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(inlet_node)

                        A[row][col] += C
                        b[row] -= C*variables.node_values[inlet_node][self.pressure_idx]
                    else:
                        boundary_value = variables.node_values[inlet_node][self.pressure_idx]
                        b[row] -= boundary_value*C

                    if outlet_node in nodes_to_solve:
                        col = nodes_to_solve.index(outlet_node)

                        A[row][col] -= C
                        b[row] += C*variables.node_values[outlet_node][self.pressure_idx]
                    else:
                        boundary_value = variables.node_values[outlet_node][self.pressure_idx]
                        b[row] += boundary_value*C

            result = np.linalg.solve(A,b)

            for i in range(size):
                variables.node_values[nodes_to_solve[i]][self.pressure_idx] += self.relaxation_factor*result[i]

            self.residual.append(self.compute_residual(properties,variables,topology,boundary_condition))

            self.solve_velocity(properties,variables,topology,boundary_condition)
        
