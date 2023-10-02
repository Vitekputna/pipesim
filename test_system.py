from pipesim import *
from conditions import set_pressure
from properties import constant_properties
from properties import CRSprop_isothermal
from components import *
import matplotlib.pyplot as plt

# import numpy as np
# from CRSprop import CRSprop

# prop = CRSprop(["N2O"])

# p = np.linspace(4,6)

# eee = []

# for val in p:
#     eee.append(prop.density("N2O",val,300))

# plt.plot(p,eee,'kx')
# plt.show()

sim = pipesim()

sim.add_pipe(1,2,diameter=0.01,length=2,N_divisions=400)
# sim.add_pipe(2,3,diameter=0.01,length=1,N_divisions=100)

# sim.variables.init_values(1e6,5e6,0.2,10)

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
sim.add_boundary_condition(set_pressure(2,4e6))

sim.solve()
 
sim.plot_velocity(length_scale=True)
sim.plot_pressure(length_scale=True)
sim.plot_density(length_scale=True)
sim.plot_residual()

