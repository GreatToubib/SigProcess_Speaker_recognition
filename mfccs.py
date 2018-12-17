from preprocess import framing
import numpy as np
from formants import hpfilter2, preEmphasis, preemphasis2
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
    x=preemphasis2(x,a)
    FL=framing(fs,x)
    
    FL=framesHamming(FL)
    
    powF=calculatePowerSpectrumFrames(FL)
    #print("dimensions de powF:",powF.shape)
    
    temp=(len(FL[0])*2)-1
    FBValues=filter_banks(powF, fs, nfilt=26 , NFFT=temp)
    #print("dimensions de FBV:",FBValues.shape)
    
    """i=0
    while i < len(FBValues):
        FBValues[i] = np.where(FBValues[i] == 0,np.finfo(float).eps,FBValues[i])
        FBValues[i]=np.log(FBValues[i])
        i=i+1"""
    
    MFCCstemp=dct(FBValues, type=2, axis=1, norm='ortho')
    #print("dimensions de MFCCs:",MFCCstemp.shape) 
    
    MFCCs=MFCCstemp[:,0:13]
    #print("dimensions de MFCCs:",MFCCs.shape) #of the obtained vectors, only the first 13 elements are kept
    
    return MFCCs
    
    