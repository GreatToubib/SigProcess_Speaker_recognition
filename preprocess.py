import math
import numpy as np

import matplotlib.pyplot as plt

def normalize(x): 
    
    Xmax = np.amax(np.abs(x)) # find maximum amplitude
    x = x/Xmax # normalization
    
    return x

def framing(fs,x): # rentrée en ms
    """ Decoupe un signal en frames , arguments: fs la frequence d'echantillonage du signal, x son amplitude, 
    width la largeur en frequence d'une frame et step le pas entre 2 frames. Return le tableau de frames"""
    width=25
    step=10
    duration = np.size(x) # Nbre d'échantillon du signal 
    width = math.floor(width*fs/1000) # convertir en nbre d'échantillon, et en integer
    step = math.floor(step*fs/1000) # convertir en nbre d'échantillon, et en integer
    framelist=[]
    f=0
    l=0
    itmax=int(duration/step)-1
    for j in range(0,itmax): #duration, step or just itmax / formants or mfccs
        l=f+width
        temp=np.asarray(x[f:l])
        """plt.figure()
        plt.plot(temp)
        plt.show()"""
        framelist.append(temp) # ajoute une frame à la liste
        f=f+step
    framelist=np.asarray(framelist)
    """print("framelist shape: ",framelist.shape)"""
    return framelist

def framing2(fs,x): # rentrée en ms
    """ Decoupe un signal en frames , arguments: fs la frequence d'echantillonage du signal, x son amplitude, 
    width la largeur en frequence d'une frame et step le pas entre 2 frames. Return le tableau de frames"""
    width=25
    step=10
    duration = np.size(x) # Nbre d'échantillon du signal 
    width = math.floor(width*fs/1000) # convertir en nbre d'échantillon, et en integer
    step = math.floor(step*fs/1000) # convertir en nbre d'échantillon, et en integer
    framelist=[]
    f=0
    l=0
    
    for j in range(0,duration,step): #duration, step or just itmax / formants or mfccs
        l=f+width
        temp=np.asarray(x[f:l])
        """plt.figure()
        plt.plot(temp)
        plt.show()"""
        framelist.append(temp) # ajoute une frame à la liste
        f=f+step
    del framelist[-1]
    framelist=np.asarray(framelist)
    
    """print("framelist shape: ",framelist.shape)"""
    return framelist
    

