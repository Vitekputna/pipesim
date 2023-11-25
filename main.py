from pipesim import pipesim
from solvers import pressure_correction_solver
from conditions import set_pressure
from properties import constant_properties
from components import pipe

# Create pipesim object
sim = pipesim()

# Configure system of components
comp = pipe(0,1)
comp.set_diameter(0.1)
comp.length = 1
sim.add_component(comp)

# Initial conditions
sim.variables.init_values(50,100,0.2,0.3)

# Set solver and settings
sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

# Set properties model and parameters
sim.set_properties_model(constant_properties)
sim.properties.set_density(1000)
sim.properties.set_viscosity(0.0001)

# sim.set_properties_model(compresible_isothermal)
# sim.properties.set_compresibility(10)
# sim.properties.set_viscosity(1e-5)

# Set boundary conditions
sim.add_boundary_condition(set_pressure(0,100))
sim.add_boundary_condition(set_pressure(1,50))

# Run solver
sim.solve()

print(sim.mass_fluxes())
# sim.plot_residual()
# sim.plot_node_values(0)
