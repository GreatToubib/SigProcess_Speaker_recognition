# -*- coding: utf-8 -*-
"""
Projet traitement du signal
"""

import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import os, random
from pitchEstimate import autocorrBasedpitch,cepstrumBasedPitch
from formants import formant
from mfccs import mfccs
from energy import energy
from preprocess import framing,framing2,normalize

from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav


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

def features(fs,x):
    PitchA=autocorrBasedpitch(fs,x)
    PitchC=cepstrumBasedPitch(fs,x)
    Mfccs=mfccs(fs,x)
    Formants=formant(fs,x)
    Energy=energy(x)
    
    return Energy, PitchA, PitchC, Formants, Mfccs

def main():
    fs, x = wavread("arctic_a0001.wav")
    """Energy, PitchA, PitchC, Formants, Mfccs=features(fs,x)
    print(Energy.shape, PitchA.shape, PitchC.shape, Formants.shape, Mfccs.shape)"""
    mf1=mfccs(fs,x)
    mf2=mfcc(x,fs,winfunc=np.hamming,ceplifter=0)
    print(mf1.shape, mf1[0,:])
    print(mf2.shape, mf2[0,:])
    
    
    

    """print(Mfccs[0,0])
    x=normalize(x)
    FL=framing(fs,x,30,15)
    E=energy(FL[0])
    print(E)"""
    
    
    """i=0    
    n=15 #nbre de fichiers
    while(i<n): 
        file=random.choice(os.listdir("male"))
    
        fs, x = wavread(file)
        Energy, PitchA, PitchC, Formants, Mfccs=features(fs,x)
        print(Energy.shape, PitchA.shape, PitchC.shape, Formants.shape, Mfccs.shape)
        i=i+1
    """

if __name__ == "__main__":
    main()








