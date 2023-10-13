from pipesim import *
from conditions import set_pressure
from discharge_models import *
from properties import *

sim = pipesim()

sim.add_pipe(0,1,0.02,1,N_divisions=50)
sim.add_valve(1,2,diameter=0.02,length = 0.05,Kv = 1e-3)
sim.add_pipe(2,3,0.02,1,N_divisions=50)


sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

sim.set_properties_model(CRSprop_isothermal)
sim.properties.set_specie("C3H8O")
sim.properties.temperature = 300

sim.add_boundary_condition(set_pressure(0,2e5))
sim.add_boundary_condition(set_pressure(3,1e5))

sim.solve()
 
sim.plot_velocity(length_scale=True)
sim.plot_pressure(length_scale=True)
sim.plot_density(length_scale=True)
sim.plot_mass_flux(length_scale=True)
sim.plot_residual()

print(np.average(sim.mass_fluxes()))