import numpy as np
import random


class variables:

    def __init__(self) -> None:
        self.values_per_node = 0
        self.values_per_component = 0

    def init_variables(self, N_nodes : int, N_components : int) -> None:
        self.node_values = np.zeros((N_nodes,self.values_per_node))
        self.component_values = np.zeros((N_components,self.values_per_component))

    def init_values(self, min_node_value : float, max_node_value : float, min_comp_value : float, max_comp_value : float) -> None:

        for i in range(len(self.node_values)):
            num = random.uniform(min_node_value,max_node_value)
            self.node_values[i] = num
            
        for i in range(len(self.component_values)):
            num = random.uniform(min_comp_value,max_comp_value)
            self.component_values[i] = num