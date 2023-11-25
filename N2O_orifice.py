#NOT WORKING
from pipesim import *
from conditions import set_pressure
from properties import CRSprop_isothermal
import numpy as np

sim = pipesim()

sim.add_pipe(0,1,0.02,1,N_divisions=50)
sim.add_orifice(1,2,0.001,0.01)

sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

sim.set_properties_model(CRSprop_isothermal)
sim.properties.set_specie("N2O")
sim.properties.temperature = 300

sim.add_boundary_condition(set_pressure(0,90e5))
sim.add_boundary_condition(set_pressure(2,50e5))

sim.solve()
print(np.average(sim.mass_fluxes())) 

sim.plot_velocity(length_scale=True)
sim.plot_pressure(length_scale=True)
sim.plot_density(length_scale=True)
sim.plot_mass_flux(length_scale=True)
sim.plot_residual()