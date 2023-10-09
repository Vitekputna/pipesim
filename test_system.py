from pipesim import *
from conditions import set_pressure
from discharge_models import *
from properties import *

sim = pipesim()

sim.add_pipe(3,4,diameter=0.01,length=0.1,N_divisions=100)
sim.add_area_change(4,5,0.02,0.001)
sim.add_orifice(5,6,0.001,0.01)

# sim.add_area_change(4,7,0.02,0.001)
# sim.add_orifice(7,6,0.001,0.01)

# sim.add_area_change(4,8,0.02,0.001)
# sim.add_orifice(8,6,0.001,0.01)

# sim.add_area_change(4,9,0.02,0.001)
# sim.add_orifice(9,6,0.001,0.01)

# sim.add_area_change(4,10,0.02,0.001)
# sim.add_orifice(10,6,0.001,0.01)

# sim.add_area_change(4,11,0.02,0.001)
# sim.add_orifice(11,6,0.001,0.01)


sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

# sim.set_properties_model(constant_properties)
# sim.properties.set_density(1000)
# sim.properties.set_viscosity(0.001)

sim.set_properties_model(CRSprop_isothermal)
sim.properties.set_specie("N2O")
sim.properties.temperature = 300

sim.add_boundary_condition(set_pressure(3,6e6))
sim.add_boundary_condition(set_pressure(6,2.5e6))

sim.solve()
 
sim.plot_velocity(length_scale=True)
sim.plot_pressure(length_scale=True)
sim.plot_density(length_scale=True)
sim.plot_mass_flux(length_scale=True)
sim.plot_residual()

