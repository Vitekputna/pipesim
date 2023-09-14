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