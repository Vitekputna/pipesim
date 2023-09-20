from pipesim import *
from conditions import set_pressure
from properties import constant_properties
from components import *
import matplotlib.pyplot as plt

sim = pipesim()

comp = general(0,1)
comp.resistance_coeff = 1
sim.add_component(comp)

comp = pipe(1,2)
comp.length = 2
comp.outlet_height = -0.001
sim.add_component(comp)

sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

sim.set_properties_model(constant_properties)
sim.properties.set_density(1000)
sim.properties.set_viscosity(1e-5)

sim.add_boundary_condition(set_pressure(0,100))
sim.add_boundary_condition(set_pressure(2,50))

sim.solve()

print(sim.variables.node_values)
print(sim.variables.component_values)

# plt.figure()
# plt.plot(sim.variables.node_values[0],'kx')
# plt.show()
# sim.plot_residual()\