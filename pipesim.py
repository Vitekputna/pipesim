import numpy as np
from topology import *
from components import *
from solvers import * 
from conditions import condition
from variables import variables
from properties import properties
import matplotlib.pyplot as plt 

class pipesim:

    def __init__(self) -> None:
        self.topology = topology()
        self.variables = variables()
        self.properties = properties()
        self.boundary_conditions = []

        self.internal_node_offset = 1000
        self.internal_nodes = [1000]

    def add_pipe(self, inlet_node : int, outlet_node : int, diameter : float, length : float, N_divisions = 10) -> None:

        for i in range(N_divisions):

            if i == 0:
                inlet = inlet_node
            else:
                inlet = outlet

            if i == N_divisions-1:
                outlet = outlet_node
            else:
                self.internal_nodes.append(self.internal_nodes[-1]+1)
                outlet = self.internal_nodes[-1]

            # print(inlet,outlet)

            comp = pipe(inlet,outlet)
            comp.length = length
            comp.set_diameter(diameter)

            self.add_component(comp)

        
    def add_area_change(self) -> None:
        pass

    def add_local_loss(self) -> None:
        pass

    def set_solver(self, solver : solver) -> None:
        self.solver = solver()

    def set_properties_model(self, model : properties) -> None:
        self.properties = model()

    def add_component(self, component : component) -> None:
        self.topology.add_component(component)

        self.variables.values_per_component = 1
        self.variables.values_per_node = 1
        self.variables.init_variables(self.topology.N_nodes,self.topology.N_components)

    def add_boundary_condition(self,boundary_condition : condition) -> None:
        self.boundary_conditions.append(boundary_condition)

    def solve(self) -> None:
        self.solver.solve(self.properties,self.variables,self.topology,self.boundary_conditions)

    def print_variables(self) -> None:
        print(self.variables.node_values)
        print(self.variables.component_values)

    def plot_residual(self) -> None:

        max_residual = np.max(self.solver.residual)

        plt.figure()
        plt.title("Residual")
        plt.yscale("log")
        plt.plot(self.solver.residual/max_residual,'x')
        plt.grid()
        plt.show()

    def plot_pressure(self, length_scale = False) -> None:
        index = self.solver.pressure_idx
        size = len(self.variables.node_values)

        length = np.linspace(0,size-1,size)

        if length_scale:
            for i in range(1,size):
                length[i] = length[i-1] + self.topology.components[i-1].length

        vector = np.zeros(size)

        for i in range(size):
            vector[i] = self.variables.node_values[i][index]

        plt.figure()
        plt.title("pressure")
        plt.plot(length,vector)
        plt.grid()

    def plot_velocity(self, length_scale = False) -> None:
        index = self.solver.velocity_idx
        size = len(self.variables.component_values)

        vector = np.zeros(2*size)
        length = np.zeros(2*size)

        for i in range(size):
            comp = self.topology.components[i]
            velocity = self.variables.component_values[i][index]

            inlet_pressure = self.variables.node_values[comp.inlet_node][self.solver.pressure_idx]
            outlet_pressure = self.variables.node_values[comp.outlet_node][self.solver.pressure_idx]
            
            area = comp.area
            inlet_area = comp.inlet_area
            outlet_area = comp.outlet_area

            inlet_density = self.properties.density(self.properties.temperature,inlet_pressure)
            outlet_density = self.properties.density(self.properties.temperature,outlet_pressure)

            density = (inlet_density+outlet_density)/2

            inlet_velocity = velocity*area*density/(inlet_area*inlet_density)
            outlet_velocity = velocity*area*density/(outlet_area*outlet_density)

            vector[2*i] = inlet_velocity
            vector[2*i+1] = outlet_velocity

            if i == 0:
                length[2*i] = 0
            else:
                length[2*i] = length[2*i-1]
            length[2*i+1] = length[2*i] + comp.length

        plt.figure()
        plt.title("velocity")
        plt.plot(length,vector)
        plt.grid()

    def mass_fluxes(self) -> np.array:
        size = len(self.variables.component_values)
        fluxes = np.zeros(size)

        for i in range(size):
            area = self.topology.components[i].area
            pressure = (self.variables.node_values[self.topology.components[i].inlet_node] + self.variables.node_values[self.topology.components[i].outlet_node])/2
            density = self.properties.density(self.properties.temperature,pressure)
            velocity = self.variables.component_values[i]

            fluxes[i] = area*density*velocity

        return fluxes

        
        
        