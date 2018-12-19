import numpy as np
def energy (x):
    """
    returns the energy of an input signal
        arguments :
            x: inout signal
        returns: 
            E: Energy of the signal
    """
    x=np.square(np.abs(x)) # mise au carré des normes
    E=np.sum(x) # somme les elements de l'array
    return E