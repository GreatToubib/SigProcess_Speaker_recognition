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
    """plt.figure()
    plt.title("signal complet")
    plt.plot(x1)
    plt.show()"""
    return fs, x1

def features(fs,x):
    PitchA=autocorrBasedpitch(fs,x)
    PitchC=cepstrumBasedPitch(fs,x)
    Formants=formant(fs,x)
    #Mfccs=mfccs(fs,x) 
    Mfccs=mfcc(x,fs,winfunc=np.hamming,ceplifter=0)
    Energy=energy(x)
    
    return Energy, PitchA, PitchC, Formants, Mfccs

def main():
    """fs, x = wavread("arctic_a0001.wav")
    Energy, PitchA, PitchC, Formants, Mfccs=features(fs,x)
    print(Energy.shape, PitchA.shape, PitchC.shape, Formants.shape, Mfccs.shape)"""
    
    """plt.figure()
    plt.subplot(3,1,1)
    plt.plot(PitchA) # energie 
    plt.title("P A")
    plt.show()
    plt.subplot(3,1,2)
    plt.plot(PitchC) # voiced or unvoiced
    plt.title("P C")
    plt.show()
    plt.subplot(3,1,3)
    plt.plot(Formants[0]) # frequences fondamentales
    plt.title("Formants")
    plt.show()"""
    
    
    """mf1=mfccs(fs,x)
    mf2=mfcc(x,fs,winfunc=np.hamming,ceplifter=0)
    print(mf1.shape, mf1[0,:])
    print(mf2.shape, mf2[0,:])"""
    
    i=0    
    n=5 #nbre de fichiers
    plt.figure()
    while(i<n): 
        file=random.choice(os.listdir("male"))
    
        fs, x = wavread(file)
        Energy, PitchA, PitchC, Formants, Mfccs=features(fs,x)
        plt.plot(PitchA) 
        #plt.title("male pitch A du: ", i)
        """plt.subplot(2,1,2)
        plt.plot(PitchC)
        #plt.title("male Pitch C du: ", i)"""
        i=i+1
    plt.show()
    
    """i=0    
    while(i<n): 
        file=random.choice(os.listdir("female"))
    
        fs, x = wavread(file)
        Energy, PitchA, PitchC, Formants, Mfccs=features(fs,x)
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(PitchA)
        #plt.title("female pitch A du: ", i)
        plt.subplot(2,1,2)
        plt.plot(PitchC) 
        #plt.title("female Pitch C du: ", i)
        i=i+1"""


if __name__ == "__main__":
    main()








