#NOT WORKING
from pipesim import *
from conditions import set_pressure
from discharge_models import *
from properties import *

sim = pipesim()

# sim.add_pipe(0,1,0.02,1,N_divisions=50)
# sim.add_valve(1,2,diameter=0.02,length = 0.05,Kv = 1.819e-8)
# sim.add_area_change(3,4,0.02,0.01)

# Model
# Nipl
sim.add_area_change(0,1,0.1063,0.016)
sim.add_pipe(1,2,0.016,0.041,N_divisions=10)
#T
sim.add_area_change(2,3,0.016,0.017)
sim.add_pipe(3,4,0.017,0.064)
#Hose tail
sim.add_area_change(4,5,0.017,0.012)
sim.add_pipe(5,6,0.012,0.0645,N_divisions=10)
#Hose
sim.add_area_change(6,7,0.012,0.016)
sim.add_pipe(7,8,0.016,1,N_divisions=100)
#Hose tail
sim.add_area_change(8,9,0.016,0.012)
sim.add_pipe(9,10,0.012,0.0645,N_divisions=10)
#T-B
sim.add_area_change(10,11,0.012,0.026)
sim.add_pipe(11,12,0.026,0.028,N_divisions=10)
#Nipl
sim.add_area_change(12,13,0.026,0.017)
sim.add_pipe(13,14,0.017,0.045,N_divisions=10)
#Solenoid
sim.add_valve(14,15,0.020,0.064,7)
#Nipl
sim.add_area_change(15,16,0.020,0.017)
sim.add_pipe(16,17,0.017,0.045,N_divisions=10)
#T-B
sim.add_area_change(17,18,0.017,0.026)
sim.add_pipe(18,19,0.026,0.028,N_divisions=10)
#Nipl
sim.add_area_change(19,20,0.026,0.017)
sim.add_pipe(20,21,0.017,0.045,N_divisions=10)
#T-B
sim.add_area_change(21,22,0.017,0.026)
sim.add_pipe(22,23,0.026,0.028,N_divisions=10)
#Hose tail
sim.add_area_change(23,24,0.026,0.0145)
sim.add_pipe(24,25,0.0145,0.077,N_divisions=10)
#Hose
sim.add_area_change(25,26,0.0145,0.019)
sim.add_pipe(26,27,0.019,0.3,N_divisions=30)
#Hose tail
sim.add_area_change(27,28,0.019,0.0145)
sim.add_pipe(28,29,0.0145,0.077,N_divisions=10)
#Injector inlet
sim.add_area_change(29,30,0.0145,0.020)
sim.add_area_change(30,31,0.020,0.015)
sim.add_area_change(31,32,0.015,0.1)



#Orifice

CD_model = linear_model
sim.add_orifice(32,33,0.0013,0.014,discharge_model=CD_model)
sim.add_orifice(32,33,0.0013,0.014,discharge_model=CD_model)
sim.add_orifice(32,33,0.0013,0.014,discharge_model=CD_model)
sim.add_orifice(32,33,0.0013,0.014,discharge_model=CD_model)
sim.add_orifice(32,33,0.0013,0.014,discharge_model=CD_model)
sim.add_orifice(32,33,0.0013,0.014,discharge_model=CD_model)

sim.set_solver(pressure_correction_solver)
sim.solver.max_iterations = 100
sim.solver.relaxation_factor = 0.8
sim.solver.pressure_idx = 0

sim.set_properties_model(CRSprop_isothermal)
sim.properties.set_specie("C3H8O")
sim.properties.temperature = 283.15

sim.add_boundary_condition(set_pressure(0,3.108e6))
sim.add_boundary_condition(set_pressure(33,2.5e6))

sim.solve()
 
sim.plot_velocity(length_scale=True,plot_nodes=True,color="r")
sim.plot_pressure(length_scale=True)
sim.plot_density(length_scale=True)
sim.plot_mass_flux(length_scale=True)
sim.plot_reynolds()
sim.plot_residual()

print(np.average(sim.mass_fluxes()))