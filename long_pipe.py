from pipesim import *
from conditions import set_pressure
from properties import constant_properties
from properties import compresible_isothermal
from components import *
import matplotlib.pyplot as plt

sim = pipesim()

length = 1
N = 500
dl = length/N

for i in range(N):
    comp = pipe(i,i+1)
    comp.length = dl
    comp.set_diameter(0.01)
    sim.add_component(comp)

sim.variables.init_values(5000,10000,0.2,10)

# Set solver and settings
sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 200
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

# Set properties model and parameters
# sim.set_properties_model(constant_properties)
# sim.properties.set_density(1000)
# sim.properties.set_viscosity(1e-5)  

sim.set_properties_model(compresible_isothermal)
sim.properties.set_compresibility(0.2e-3)
sim.properties.set_viscosity(1e-5)

# Set boundary conditions
sim.add_boundary_condition(set_pressure(0,5e6))
sim.add_boundary_condition(set_pressure(N,1e6))

# Run solver
sim.solve()

sim.plot_component_values(0)
sim.plot_node_values(0)
sim.plot_residual()
plt.show()