from preprocess import framing
import numpy as np
from formants import preEmphasis
from scipy import signal
from scipy.fftpack import dct
from filterbanks import filter_banks

def framesHamming(frameList):
    """ applies an hamming window to each frame of a framelist
    arguments : frameList, array-like of  frames of a given signal
    returns: HammerFrames: array-like of power spectrum frames of the given signal
    """
    i=0
    hammerFrames=[]
    while i < len(frameList):
        w=signal.hamming(len(frameList[i])) #hamming window
        frameList[i]= w*frameList[i] # apply the hamming window to each frame
        hammerFrames.append(frameList[i])
        i=i+1
    hammerFrames=np.asarray(hammerFrames)
    return hammerFrames

def calculatePowerSpectrumFrames(frameList):
    """ calculates the power spectrum frames of a signal.
        arguments : frameList, array-like of  frames of a given signal
        returns: powF: array-like of power spectrum frames of the given signal"""
    i=0
    NTFD=512
    powF=[]
    while i < len(frameList):
        frameList[i]=(np.square(np.abs(np.fft.fft(frameList[i]))))/NTFD
        powF.append(frameList[i])
        i=i+1
    powF=np.asarray(powF)
    return powF
    
def mfccs(fs,x):
    
    """ Computes MFCC of an input signal
        arguments: 
            fs: sampling frequency
            x: inout signal
        returns: MFCCs: array-like containing the first 13 mffccs, 
                        the first one being equivalent to the energy
    
    """
    a=0.97 # pre emphasis coefficient.
    x=preEmphasis(x,a)
    FL=framing(fs,x)
    
    FL=framesHamming(FL)
    
    powF=calculatePowerSpectrumFrames(FL)
    
    temp=(len(FL[0])*2)-1
    FBValues=filter_banks(powF, fs, nfilt=26 , NFFT=temp) # NFFT=temp, we adjust NFFT for each signal.
    
    MFCCs=dct(FBValues, type=2, axis=1, norm='ortho')
    
    MFCCs=MFCCs[:,0:13] # keeps only the first 13 coefficients for each frame.
    
    return MFCCs
    
    