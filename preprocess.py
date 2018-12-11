import math
import numpy as np

def normalize(x): 
    
    Xmax = np.amax(np.abs(x)) # find maximum amplitude
    x = x/Xmax # normalization
    
    return x

def framing(fs,x,width,step): # rentrée en ms
    """ Decoupe un signal en frames , arguments: fs la frequence d'echantillonage du signal, x son amplitude, 
    width la largeur en frequence d'une frame et step le pas entre 2 frames. Return le tableau de frames"""
    
    duration = np.size(x) # Nbre d'échantillon du signal 
    width = math.floor(width*fs/1000) # convertir en nbre d'échantillon, et en integer
    step = math.floor(step*fs/1000) # convertir en nbre d'échantillon, et en integer
    framelist=[]
    f=0
    l=0
    for j in range(0,duration,step): 
        l=f+width
        framelist.append(x[f:l]) # ajoute une frame à la liste
        f=f+step
       
    return framelist
    

