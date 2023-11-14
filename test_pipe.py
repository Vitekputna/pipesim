from pipesim import *
from conditions import set_pressure
from discharge_models import *
from properties import *

sim = pipesim()

sim.add_pipe(0,1,0.02,1,N_divisions=100)
sim.add_valve(1,2,diameter=0.02,length = 0.05,Kv = 1.819e-8)
sim.add_pipe(2,3,0.02,0.3,N_divisions=100)
sim.add_area_change(3,4,0.02,0.01)
sim.add_pipe(4,5,0.01,1,N_divisions=100)

sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 500
sim.solver.relaxation_factor = 0.98
sim.solver.pressure_idx = 0

sim.set_properties_model(CRSprop_isothermal)
sim.properties.set_specie("N2O")
sim.properties.temperature = 300

sim.add_boundary_condition(set_pressure(0,5e6))
sim.add_boundary_condition(set_pressure(5,2.5e6))

sim.solve()
 
sim.plot_velocity(length_scale=True,plot_nodes=True)
sim.plot_pressure(length_scale=True,plot_nodes=True)
sim.plot_density(length_scale=True,plot_nodes=True,color='b')
sim.plot_mass_flux(length_scale=True)
sim.plot_residual()

print(np.average(sim.mass_fluxes()))