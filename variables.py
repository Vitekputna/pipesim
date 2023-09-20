import numpy as np

class variables:

    def __init__(self) -> None:
        self.values_per_node = 0
        self.values_per_component = 0

    def init_variables(self, N_nodes : int, N_components : int) -> None:
        # self.node_values = np.zeros((self.values_per_node,N_nodes))
        # self.component_values = np.zeros((self.values_per_component,N_components))

        self.node_values = np.zeros((N_nodes,self.values_per_node))
        self.component_values = np.zeros((N_components,self.values_per_component))