from pipesim import pipesim, pressure_correction_solver
from conditions import set_pressure
from properties import CRSprop_isothermal

sim = pipesim()

sim.add_pipe(1,2,diameter=0.01,length=0.5,N_divisions=50)
sim.add_local_loss(2,3,0.01,0.01,10)
sim.add_pipe(3,4,diameter=0.01,length=0.1,N_divisions=50)

sim.add_area_change(4,5,0.02,0.001)
sim.add_orifice(5,6,0.001,0.01)

sim.add_area_change(4,7,0.02,0.001)
sim.add_orifice(7,6,0.001,0.01)

sim.add_area_change(4,8,0.02,0.001)
sim.add_orifice(8,6,0.001,0.01)

sim.add_area_change(4,9,0.02,0.001)
sim.add_orifice(9,6,0.001,0.01)

sim.add_area_change(4,10,0.02,0.001)
sim.add_orifice(10,6,0.001,0.01)

sim.add_area_change(4,11,0.02,0.001)
sim.add_orifice(11,6,0.001,0.01)


sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.9
sim.solver.pressure_idx = 0

sim.set_properties_model(CRSprop_isothermal)
sim.properties.set_specie("C3H8O")
sim.properties.temperature = 300

sim.add_boundary_condition(set_pressure(1,6e6))
sim.add_boundary_condition(set_pressure(6,2.5e6))

sim.solve()
 
sim.plot_velocity(length_scale=True)
sim.plot_pressure(length_scale=True)
sim.plot_density(length_scale=True)
sim.plot_mass_flux(length_scale=True)
sim.plot_residual()

print(sim.mass_fluxes())
