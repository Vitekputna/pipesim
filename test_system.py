from pipesim import *
from conditions import set_pressure
from properties import constant_properties
from properties import CRSprop_isothermal
from components import *
import matplotlib.pyplot as plt

sim = pipesim()

# sim.add_pipe(0,10,1,1,10)

comp = pipe(0,1)
comp.length = 1
comp.roughness = 0.045
comp.set_diameter(0.03)
sim.add_component(comp)

comp = general(1,2)
comp.length = 0.01
comp.set_diameter(0.03)
comp.resistance_coeff = 100
sim.add_component(comp)

comp = pipe(2,3)
comp.length = 1
comp.roughness = 0.045
comp.set_diameter(0.03)
sim.add_component(comp)

comp = general(3,4)
comp.length = 0.01
comp.set_inlet_diameter(0.03)
comp.set_outlet_diameter(0.025)
comp.resistance_coeff = 100
sim.add_component(comp)

comp = pipe(4,5)
comp.length = 0.5
comp.roughness = 0.045
comp.set_diameter(0.025)
sim.add_component(comp)

sim.variables.init_values(1e6,5e6,0.2,10)

sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 250
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

# sim.set_properties_model(constant_properties)
# sim.properties.set_density(1000)
# sim.properties.set_viscosity(0.001) 

sim.set_properties_model(CRSprop_isothermal)
sim.properties.set_specie("N2O")
sim.properties.temperature = 300

sim.add_boundary_condition(set_pressure(0,6e6))
sim.add_boundary_condition(set_pressure(5,2.5e6))

sim.solve()

sim.plot_velocity(length_scale=True)
sim.plot_pressure(length_scale=True)
sim.plot_residual()

print(sim.mass_fluxes())
plt.show()