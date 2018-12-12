from preprocess import framing
import numpy as np
from formants import hpfilter2
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import dct
from filterbanks import filter_banks

def framesHamming(FL):
    i=0
    while i < len(FL):
        w=signal.hamming(len(FL[i])) #hamming window
        FL[i]= w*FL[i] # apply the hamming window to each frame
        i=i+1
    return FL

def calculatePowerSpectrumFrames(FL):
    i=0
    NTFD=512
    while i < len(FL):
        FL[i]=(np.square(np.abs(np.fft.fft(FL[i]))))/NTFD
        i=i+1
    return FL
    
def mfccs(fs,x):
    a=0.97 # a for mfcc
    x=hpfilter2(fs,x,a)
    FL=framing(fs,x,30,15)
    
    FL=framesHamming(FL)
    
    powF=calculatePowerSpectrumFrames(FL)
    #print("dimensions de powF:",powF.shape)
    
    FBValues=filter_banks(powF, fs, nfilt=40, NFFT=958)
    #print("dimensions de FBV:",FBValues.shape)
    
    MFCCstemp=dct(FBValues, type=2, axis=1, norm='ortho')
    #print("dimensions de MFCCs:",MFCCstemp.shape) 
    
    MFCCs=MFCCstemp[:,0:13]
    #print("dimensions de MFCCs:",MFCCs.shape) #of the obtained vectors, only the first 13 elements are kept
    
    return MFCCs
    
    