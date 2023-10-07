
def sudden_expansion(inlet_area : float, outlet_area : float) -> float:
    #source Borda-Carnot loss https://en.wikipedia.org/wiki/Borda–Carnot_equation
    return (1-inlet_area/outlet_area)**2

def sudden_contraction(inlet_area : float, outlet_area : float) -> float:
    #source https://en.wikipedia.org/wiki/Borda–Carnot_equation
    mu = 0.63+0.37*(outlet_area/inlet_area)**3
    return ((1/mu-1)*(inlet_area/outlet_area))**2