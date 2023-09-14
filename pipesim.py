import numpy as np
from topology import *
from solvers import * 
from conditions import condition
from variables import variables
from properties import properies

class pipesim:

    def __init__(self) -> None:
        self.topology = topology()
        self.variables = variables()
        self.properties = properies()
        self.boundary_conditions = []

    def set_solver(self, solver : solver) -> None:
        self.solver = solver()

    def set_properties_model(self, model : properies) -> None:
        self.properties = model

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

    

    

    


