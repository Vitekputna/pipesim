from pipesim import *
from conditions import set_pressure
from properties import constant_properties
from topology import super_pipe

p = super_pipe(0,1)
p.inlet_area = 1
p.outlet_area = 0.05
p.inlet_height = 0
p.outlet_height = 0
p.resistance_coeff = 0
p.length = 1

flow = p.get_coeff(100,50,1200,1000)*(100-50)

print(p.bernouli_residual(flow,100,50,1200,1000))

# sim = pipesim()

# comp1 = pipe(0,1)
# comp1.length = 1
# comp1.diameter = 1e-2
# comp2 = pipe(1,2)
# comp3 = pipe(2,3)
# comp4 = pipe(3,4)
# comp5 = pipe(3,5)

# sim.add_component(comp1)
# sim.add_component(comp2)
# sim.add_component(comp3)
# sim.add_component(comp4)
# # sim.add_component(comp5)

# sim.set_solver(pressure_correction_solver)

# sim.set_properties_model(constant_properties)
# sim.properties.set_density = 1000
# sim.properties.set_viscosity = 1e-5

# sim.add_boundary_condition(set_pressure(0,100))
# sim.add_boundary_condition(set_pressure(4,50))
# # sim.add_boundary_condition(set_pressure(5,50))

# sim.solve()

# print(sim.variables.node_values)

# # sim.print_variables()