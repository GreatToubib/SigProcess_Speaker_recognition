import numpy as np
def energy (x):
    
    x=np.square(np.abs(x)) # mise au carré des normes
    E=np.sum(x) # somme les elements de l'array
    return E