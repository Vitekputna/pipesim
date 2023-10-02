import numpy as np

def laminar(Re : float) -> float:
    # return 64/(Re+1e-6)
    return 0.02


def Churchill(Re : float, eps : float, diameter : float) -> float:
    # https://hal.science/hal-01586547/document eq12

    return 0.02
    # C1 = (2.457*np.log(1/( (7/Re)**0.9 + 0.27*eps/diameter)))**16

    # C2 = (37530/Re)**16

    # return 8*( (8/Re)**12 + 1/((C1+C2)**1.5) )**(1/12)


