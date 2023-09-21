from pipesim import *
from conditions import set_pressure
from properties import constant_properties
from properties import compresible_isothermal
from components import *

# Create pipesim object
sim = pipesim()

# Configure system of components
comp = general(0,1)
comp.resistance_coeff = 1
sim.add_component(comp)

comp = general(1,2)
comp.resistance_coeff = 1
sim.add_component(comp)

comp = general(2,3)
comp.resistance_coeff = 1
sim.add_component(comp)

comp = general(3,4)
comp.resistance_coeff = 1
sim.add_component(comp)

comp = general(4,5)
comp.resistance_coeff = 1
sim.add_component(comp)

# Initial conditions
sim.variables.init_values(50,100,0.2,0.3)

# Set solver and settings
sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

# Set properties model and parameters
# sim.set_properties_model(constant_properties)
# sim.properties.set_density(1000)
# sim.properties.set_viscosity(1e-5)

sim.set_properties_model(compresible_isothermal)
sim.properties.set_compresibility(10)
sim.properties.set_viscosity(1e-5)

# Set boundary conditions
sim.add_boundary_condition(set_pressure(0,100))
sim.add_boundary_condition(set_pressure(5,50))

# Run solver
sim.solve()

# Print results
print(sim.variables.node_values)
print(sim.variables.component_values)

sim.plot_residual()
sim.plot_node_values(0)
