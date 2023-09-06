from pipesim import *

sim = pipesim()

comp1 = pipe(0,1)
comp1.length = 1
comp1.diameter = 1e-2
comp2 = pipe(1,2)
comp3 = pipe(2,3)
comp4 = pipe(3,4)

sim.add_component(comp1)
sim.add_component(comp2)
sim.add_component(comp3)
sim.add_component(comp4)

sim.set_solver(pressure_correction_solver)

sim.add_boundary_condition(set_pressure(0,100))
sim.add_boundary_condition(set_pressure(4,50))

sim.solve()

# sim.print_variables()