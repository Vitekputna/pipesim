from pipesim import *

# comp1 = component(0,1)
# comp2 = component(1,2)
# comp3 = component(2,3)
# comp4 = component(1,3)
# comp5 = component(4,3)
# comp6 = component(4,0)

# sim = topology()

# sim.add_component(comp1)
# sim.add_component(comp2)
# sim.add_component(comp3)
# sim.add_component(comp4)
# sim.add_component(comp5)
# sim.add_component(comp6)

# sim.print()

sim = pipesim([1,1],[1,3])
sim.set_solver(pressure_correction_solver)
sim.solve()

sim.print_variables()