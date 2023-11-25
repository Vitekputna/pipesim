import numpy as np
import random
from topology import topology

class variables:

    def __init__(self) -> None:
        self.values_per_node = 0
        self.values_per_component = 0

        # self.node_values = np.array(1)
        # self.component_values = np.array(1)

        self.node_hash_table = {}

    def create_hash_table(self,topology : topology) -> None:

        keys = list(topology.nodes.keys())

        for i in range(topology.N_nodes):
            key = keys[i]
            self.node_hash_table[key] = i

    def init_variables(self, N_nodes : int, N_components : int) -> None:
        self.node_values = np.zeros((N_nodes,self.values_per_node))
        self.component_values = np.zeros((N_components,self.values_per_component))

    def init_values(self, min_node_value : float, max_node_value : float, min_comp_value : float, max_comp_value : float,
                    node_idxs_to_init : list = [], comp_idxs_to_init : list = []) -> None:

        print("Initializing values")

        if len(node_idxs_to_init) == 0:
            node_idxs_to_init = range(self.values_per_node)

        if len(comp_idxs_to_init) == 0:
            comp_idxs_to_init = range(self.values_per_component)

        for i in range(len(self.node_values)):
            num = random.uniform(min_node_value,max_node_value)
            for j in node_idxs_to_init:
                self.node_values[i][j] = num
            
        for i in range(len(self.component_values)):
            num = random.uniform(min_comp_value,max_comp_value)
            for j in comp_idxs_to_init:
                self.component_values[i][j] = num

    def init_node_value(self, index : int, value):
        
        for i in range(len(self.node_values)):
            self.node_values[i][index] = value

    def init_component_value():
        pass

    def node_value(self, node_idx : int):
        return self.node_values[self.node_hash_table[node_idx]]