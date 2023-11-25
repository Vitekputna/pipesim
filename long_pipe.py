from pipesim import pipesim
from solvers import pressure_correction_solver
from conditions import set_pressure
from properties import constant_properties
from components import pipe
import matplotlib.pyplot as plt

sim = pipesim()

length = 10
N = 500
dl = length/N

for i in range(N):
    comp = pipe(i,i+1)
    comp.length = dl
    comp.set_diameter(0.005)
    sim.add_component(comp)

sim.variables.init_values(1e6,5e6,0.2,10)

# Set solver and settings
sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 250
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

# Set properties model and parameters
sim.set_properties_model(constant_properties)
sim.properties.set_density(1000)
sim.properties.set_viscosity(1e-5)  

# sim.set_properties_model(compresible_isothermal)
# sim.properties.set_compresibility(0.2e-3)
# sim.properties.set_viscosity(1e-5)

# sim.set_properties_model(CRSprop_isothermal)
# sim.properties.set_specie("C3H8O")
# sim.properties.temperature = 280

# Set boundary conditions
sim.add_boundary_condition(set_pressure(0,10e6))
sim.add_boundary_condition(set_pressure(N,2.5e6))

# Run solver
sim.solve()

sim.plot_residual()

plt.show()
