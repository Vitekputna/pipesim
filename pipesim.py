import numpy as np
from topology import *
from components import *
from solvers import * 
from conditions import condition
from variables import variables
from properties import properties
from discharge_models import discharge_model, linear_model
import matplotlib.pyplot as plt 

class pipesim:

    def __init__(self) -> None:
        self.topology = topology()
        self.variables = variables()
        self.properties = properties()
        self.boundary_conditions = []

        self.internal_node_offset = 1000
        self.internal_nodes = []

    def add_pipe(self, inlet_node : int, outlet_node : int, diameter : float, length : float, N_divisions = 10) -> None:

        dl = length/N_divisions

        for i in range(N_divisions):
            if i == 0:
                inlet = inlet_node
            else:
                inlet = outlet

            if i == N_divisions-1:
                outlet = outlet_node
            else:

                if len(self.internal_nodes) == 0:
                    self.internal_nodes.append(self.internal_node_offset)
                    outlet = self.internal_nodes[-1]    
                else:
                    self.internal_nodes.append(self.internal_nodes[-1]+1)
                    outlet = self.internal_nodes[-1]

            comp = pipe(inlet,outlet)
            comp.length = dl
            comp.set_diameter(diameter)
            self.add_component(comp)

        self.variables.create_hash_table(self.topology)
       
    def add_area_change(self, inlet_node:int, outlet_node:int, inlet_diameter:float, outlet_diameter:float) -> None:
        comp = area_change(inlet_node,outlet_node)
        comp.set_diameters(inlet_diameter,outlet_diameter)
        comp.length = 0.01
        self.add_component(comp)

        self.variables.create_hash_table(self.topology)

    def add_local_loss(self, inlet_node :int, outlet_node : int, diameter : float, length : float, resistance_coefficient : float) -> None:
        comp = general(inlet_node,outlet_node)
        comp.set_diameter(diameter)
        comp.length = length
        comp.resistance_coeff = resistance_coefficient
        self.add_component(comp)

        self.variables.create_hash_table(self.topology)

    def add_orifice(self, inlet_node :int, outlet_node : int, diameter : float, length : float, discharge_model : discharge_model = linear_model) -> None:
        comp = orifice(inlet_node,outlet_node)
        comp.set_diameter(diameter)
        comp.length = length
        comp.set_discharge_model(discharge_model(length,diameter))
        self.add_component(comp)

        self.variables.create_hash_table(self.topology)

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

        if boundary_condition.index in self.topology.nodes:
            self.boundary_conditions.append(boundary_condition)
        else:
            print("Error node in boundary condition is not defined")
            exit()

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

            inlet_pressure = self.variables.node_value(comp.inlet_node)[self.solver.pressure_idx]
            outlet_pressure = self.variables.node_value(comp.outlet_node)[self.solver.pressure_idx]
            
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

    def plot_density(self, length_scale = False) -> None:
        index = self.solver.velocity_idx
        size = len(self.variables.component_values)

        vector = np.zeros(2*size)
        length = np.zeros(2*size)

        for i in range(size):
            comp = self.topology.components[i]

            inlet_pressure = self.variables.node_value(comp.inlet_node)[self.solver.pressure_idx]
            outlet_pressure = self.variables.node_value(comp.outlet_node)[self.solver.pressure_idx]

            inlet_density = self.properties.density(self.properties.temperature,inlet_pressure)
            outlet_density = self.properties.density(self.properties.temperature,outlet_pressure)

            vector[2*i] = inlet_density
            vector[2*i+1] = outlet_density

            if i == 0:
                length[2*i] = 0
            else:
                length[2*i] = length[2*i-1]
            length[2*i+1] = length[2*i] + comp.length

        plt.figure()
        plt.title("density")
        plt.plot(length,vector)
        plt.grid()

    def plot_mass_flux(self, length_scale = False) -> None:

        component_mass_flux = self.mass_fluxes()

        size = len(self.variables.component_values)
        length = np.zeros(2*size)
        node_mass_flux = np.zeros(2*size)

        if length_scale:
            for i in range(size):
                comp = self.topology.components[i]

                node_mass_flux[2*i] = component_mass_flux[i]
                node_mass_flux[2*i+1] = component_mass_flux[i]

                if i == 0:
                    length[2*i] = 0
                else:
                    length[2*i] = length[2*i-1]
                length[2*i+1] = length[2*i] + comp.length

        plt.figure()
        plt.title("Hmotnostní tok")

        if length_scale:
            plt.plot(length,node_mass_flux)
        else:
            plt.plot(node_mass_flux)
        plt.grid()

    def mass_fluxes(self) -> np.array:

        return self.solver.solve_mass_flux(self.properties,self.variables,self.topology,self.boundary_conditions)

        # size = len(self.variables.component_values)
        # fluxes = np.zeros(size)

        # for i in range(size):
        #     area = self.topology.components[i].area
        #     pressure = (self.variables.node_value(self.topology.components[i].inlet_node) + self.variables.node_value(self.topology.components[i].outlet_node))/2
        #     density = self.properties.density(self.properties.temperature,pressure)
        #     velocity = self.variables.component_values[i]

        #     fluxes[i] = area*density*velocity

        # return fluxes

        
        
        