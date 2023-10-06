from pipesim import *
from conditions import set_pressure
from properties import *

sim = pipesim()

sim.add_pipe(1,2,diameter=0.01,length=3,N_divisions=100)
sim.add_local_loss(2,3,0.01,0.01,10)
sim.add_pipe(3,4,diameter=0.01,length=3,N_divisions=100)

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

sim.add_boundary_condition(set_pressure(1,6e6))
sim.add_boundary_condition(set_pressure(4,4e6))

sim.solve()
 
sim.plot_velocity(length_scale=True)
sim.plot_pressure(length_scale=True)
sim.plot_density(length_scale=True)
sim.plot_mass_flux(length_scale=True)
sim.plot_residual()

