# -*- coding: utf-8 -*-
"""
Projet traitement du signal
"""

import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import os, random
from pitchEstimate import findPitch
from formants import formant
from mfccs import mfccs
from energy import energy

"""from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
# library to calculates mfccs

"""


def wavread(folder,file):
    os.chdir(folder)
    fs, x1 = read(file)
    os.chdir("..")
    x1=np.asarray(x1)
    """print("WAV File: ",x,"Fs:",fs, "Hz")
    plt.figure()
    plt.title("signal complet")
    plt.plot(x1)
    plt.show()"""
    return fs, x1

def features(fs,x):
    """ computes different features of an input signal
    arguments:
        fs: sampling frequency ( int )
        x: input signal ( array-like )
    returns : 
        Energy: total energy of the signal (int )
        PitchA: Fundamental frequencies using auto correlation ( array-like)
        PitchC: fundamental frequencies using ceptsurm based method ( array-like)
        Formants: Formants of each frame of the input signal ( array-like)
        Mfccs: mffcs of each frame of the input signal ( array-like)
        
        """
    
    PitchA=findPitch(fs,x,0) # 0 for autocorrelation method
    PitchC=findPitch(fs,x,1) # 1 for cepstrum based method
    Formants=formant(fs,x)
    Mfccs=mfccs(fs,x) 
    #Mfccs=mfcc(x,fs,winfunc=np.hamming,ceplifter=0) # mfccs from python speech features library
    Energy=energy(x)
    
    return Energy, PitchA, PitchC, Formants, Mfccs

def main():
    """ implementing a rule based system that sorts voice signals 
    as belonging to a male speaker or a female speaker"""
    fs, x = wavread("male","arctic_a0001.wav")
    Energy, PitchA, PitchC, Formants, Mfccs=features(fs,x)
    #print(Energy.shape, PitchA.shape, PitchC.shape, Formants.shape, Mfccs.shape)
    
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(PitchA) 
    plt.title("P A")
    plt.show()
    plt.subplot(2,1,2)
    plt.plot(PitchC) 
    plt.title("P C")
    plt.show()
    print(Formants[0])
    print(Formants[20])
    print(Formants[50])
    
    """i=0    
    n=5 #nbre de fichiers
    plt.figure()
    while(i<n): 
        folder="male"
        file=random.choice(os.listdir(folder))
        
        fs, x = wavread(folder,file)
        Energy, PitchA, PitchC, Formants, Mfccs=features(fs,x)
        plt.plot(PitchA) 
        #plt.title("male pitch A du: ", i)
        plt.subplot(2,1,2)
        plt.plot(PitchC)
        #plt.title("male Pitch C du: ", i)
        i=i+1
    plt.show()"""
    
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








