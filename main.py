from pipesim import *
from conditions import set_pressure
from properties import constant_properties
from topology import *

sim = pipesim()

comp = general(0,1)
comp.resistance_coeff = 1
sim.add_component(comp)

comp = general(1,2)
comp.resistance_coeff = 2
sim.add_component(comp)

comp = pipe(2,3)
comp.length = 10
comp.diameter = 1
sim.add_component(comp)

sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100

sim.set_properties_model(constant_properties)
sim.properties.set_density(1000)
sim.properties.set_viscosity(1e-5)

sim.add_boundary_condition(set_pressure(0,100))
sim.add_boundary_condition(set_pressure(3,50))

sim.solve()

print(sim.variables.node_values)
print(sim.variables.component_values)
# sim.plot_residual()