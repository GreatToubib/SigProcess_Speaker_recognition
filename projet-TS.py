# -*- coding: utf-8 -*-
"""
Projet traitement du signal
"""

import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import os, random
from pitchEstimate import autocorrBasedpitch,cepstrumBasedPitch
from formants import formant,hpfilter, hpfilter2, preEmphasis
from mfccs import mfccs


def wavread(x):
    os.chdir("male")
    fs, x1 = read(x)
    os.chdir("..")
    x1=np.asarray(x1)
    print("WAV File: ",x,"Fs:",fs, "Hz")
    plt.figure()
    plt.title("signal complet")
    plt.plot(x1)
    plt.show()
    return fs, x1

def main():
    fs, x = wavread("arctic_a0001.wav")
    #autocorrBasedpitch(fs,x)
    #cepstrumBasedPitch(fs,x)
    #formant(fs,x)
    #hpfilter(fs,x)
    #hpfilter2(fs,x)
    #a=0.67
    #preEmphasis(fs,x,a)
    mfccs(fs,x)
    
    """ 
    i=0    
    n=1 #nbre de fichiers
    while(i<n): 
        file=random.choice(os.listdir("male"))
    
        fs, x = wavread(file)
        autocorrBasedpitch(fs,x)
        cepstrumBasedPitch(x)
        i=i+1
    """

if __name__ == "__main__":
    main()








