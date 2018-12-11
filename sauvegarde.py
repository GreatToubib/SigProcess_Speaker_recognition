# -*- coding: utf-8 -*-
"""
Projet traitement du signal
"""

import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import math
from scipy import signal
from scipy.fftpack import dct
import os, random
from filterbanks import filter_banks
from preprocess import *
"""from scikits.talkbox.linpred.levinson_lpc import lpc"""


def wavread(x):
    os.chdir("male")
    fs, x1 = read(x)
    os.chdir("..")
    x1=np.asarray(x1)
    x1=normalize(x1)
    print("Fs:",fs, "Hz")
    plt.figure()
    plt.title("signal complet normalisé")
    plt.plot(x1)
    plt.show()
    return fs, x1


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
    
def energy (x):
    
    x=np.square(np.abs(x)) # mise au carré des normes
    E=np.sum(x) # somme les elements de l'array
    return E
    
def estimateF0(xFrame,fs):
    """autocorr Based"""

    F0=0
    lags,c, line, b=plt.xcorr(xFrame, xFrame, normed=True, usevlines=True, maxlags=320) # c = taux de correlation, l'ordonnée. 50Hz => 320
    plt.title("xcorr empilement")
    #affichage chelou, ils s'empilent tous?
    peaks, _=signal.find_peaks(c)
    middleIndex = int((np.size(peaks) - 1)/2)
    if(np.size(peaks) != 1):
        T0=(peaks[middleIndex+1]-peaks[middleIndex])
        F0=1/T0*fs

    return F0

def autocorrBasedpitch(fs,x):
    
    FL=np.asarray(framing(fs,x,30,15))
    E=[]
    VorU= [] #voice or unvoiced frame?
    F0s=[]
    threshold = 5
    for i in range (0,len(FL)):
        Ef=energy(FL[i])
        E.append(Ef)
        if Ef > threshold:
            VorU.append(1) # voiced
            F0s.append(estimateF0(FL[i],fs))
        else:
            VorU.append(0) # unvoiced
            F0s.append(0)
            
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(E) # energie 
    plt.title("Energie par Frame")
    plt.subplot(3,1,2)
    plt.plot(VorU) # voiced or unvoiced
    plt.title("Voiced/unvoiced frame?")
    plt.subplot(3,1,3)
    plt.plot(F0s) # frequences fondamentales
    plt.title("fréquences fondamentales par frame")
    
def SestimateF0(xFrame,fs):
    F0=0
    
    w, h = signal.freqz(xFrame)
    h=np.fft.ifft(20 * np.log10(abs(h)))
    """plt.figure()
    plt.plot(h)"""
    peaks, _=signal.find_peaks(h)
    """ on est dans un domaine temporel"""
    peaksvalues=[]
    for i in range (10,len(peaks)-10,1):
       peaksvalues.append(h[i]) 

    F0=np.argmax(peaksvalues)
    return F0

def cepstrumBasedPitch(fs,x):
    FL=framing(fs,x,30,15)
    E=[]
    VorU= [] #voice or unvoiced frame?
    F0s=[]
    threshold = 5
    for i in range (0,len(FL)):
        Ef=energy(FL[i])
        E.append(Ef)
        if Ef > threshold:
            VorU.append(1) # voiced
            F0s.append(SestimateF0(FL[i],fs))
        else:
            VorU.append(0) # unvoiced
            F0s.append(0)
      
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(E) # energie 
    plt.subplot(3,1,2)
    plt.plot(VorU) # voiced or unvoiced
    plt.subplot(3,1,3)
    plt.plot(F0s) # frequences fondamentales

def hpfilter(fs,x): 
    """ butter filter """
    N=1 #order
    cutoff_Hz=(fs*0.1) # cutoff frequency, frequencies below this will be deleted
    b,a =signal.butter(N,cutoff_Hz/(fs/2),'highpass') #butter filter
    
    xfiltered= signal.lfilter(b, a, x, axis=-1, zi=None) #apply filter to a signal

    plt.figure()
    plt.plot(xfiltered)
    plt.title("butter")
    return xfiltered

def hpfilter2(fs,x):
    """https://stackoverflow.com/questions/25107806/estimate-formants-using-lpc-in-python"""
    xfiltered=signal.lfilter([1], [1., 0.67], x)
    plt.figure()
    plt.plot(x)
    plt.title("hp")
    return xfiltered

def preEmphasis(fs,x,a):
    """ simple application de la formule Formants, point 2."""
    temp=np.zeros(len(x)-1)
    i=1
    while i <= len(x)-1:
        temp[i-1]=x[i]-a*x[i-1]
        i=i+1
        
    """plt.figure()
    plt.plot(temp)
    plt.title("emphasized")"""
    
    return temp

def framesHamming(FL):
    i=0
    while i < len(FL):
        w=signal.hamming(len(FL[i])) #hamming window
        FL[i]= FL[i]*np.diag(w) # apply the hamming window to each frame
        i=i+1
    return FL

def formant(fs,x):
    FL=np.asarray(framing(fs,x,30,15))
    a=0.63 #0,63 for pre emphasis
    i=0
    while i < len(FL):
        FL[i]=preEmphasis(fs, FL[i], a) # or other hp filter option ?
        w=signal.hamming(len(FL[i]))
        FL[i]= FL[i]*np.diag(w)
        """FL[i], e, k=lpc(FL[i],(2+fs/1000), axis=-1)"""
        """ 
        a : array-like
            the solution of the inversion.
        e : array-like
            the prediction error.
        k : array-like
            reflection coefficients.
        """
        FL[i]=np.sqrt(FL[i]) #roots of the lpc's => the formants
        i=i+1
     
def powerSpectrumFrames(FL,NTFD):
    i=0
    while i < len(FL):
        FL[i]=(np.square(np.abs(np.fft.fft(FL[i]))))/(2*NTFD)
        i=i+1
    return FL
    
def mfccs(fs,x):
    a=0.97 # a for mfcc
    x=preEmphasis(fs,x,a)
    FL=np.asarray(framing(fs,x,30,15))
    FL=framesHamming(FL)
    NTFD=512
    PowerSpect=powerSpectrumFrames(FL, NTFD)
    """FiltBankValues=filter_banks(np.transpose(PowerSpect), fs, nfilt=40, NFFT=512)"""
    """MFCCsVectors=dct(FiltBankValues, type=2, axis=1, norm='ortho')"""
    """ 7. of the obtaine vector or vectors? only the first 13 elements are kept"""
    print("ici")
    
fs, x = wavread("arctic_a0001.wav")
"""autocorrBasedpitch(fs,x)"""
"""formant(fs,x)"""
"""hpfilter(fs,x)
hpfilter2(fs,x)"""
mfccs(fs,x)


""" 
i=0    
while(i<1): # nbre de fichiers
    file=random.choice(os.listdir("male"))

    fs, x = wavread(file)
    autocorrBasedpitch(fs,x)
    cepstrumBasedPitch(x)
    i=i+1
    """

"""fs, x1 = wavread('arctic_a0001.wav')
autocorrBasedpitch(x1)


fs, x2 = wavread('arctic_a0002.wav')
pitch(x2)

fs, x3 = wavread('arctic_a0003.wav')
pitch(x3)

fs, x4 = wavread('arctic_a0004.wav')
pitch(x4)
"""





