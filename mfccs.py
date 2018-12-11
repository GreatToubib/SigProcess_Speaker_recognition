from preprocess import framing
import numpy as np
from formants import preEmphasis
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import dct
from filterbanks import filter_banks

def framesHamming(FL):
    i=0
    while i < len(FL):
        w=signal.hamming(len(FL[i])) #hamming window
        FL[i]= FL[i]*np.diag(w) # apply the hamming window to each frame
        i=i+1
    return FL

def powerSpectrumFrames(FL,NTFD):
    i=0
    while i < len(FL):
        FL[i]=(np.square(np.abs(np.fft.fft(FL[i]))))/(2*NTFD)
        i=i+1
    return FL
    
def mfccs(fs,x):
    print("mfccs")
    a=0.97 # a for mfcc
    x=preEmphasis(fs,x,a)
    FL=np.asarray(framing(fs,x,30,15))
    FL=framesHamming(FL)
    NTFD=512
    PowerSpect=powerSpectrumFrames(FL, NTFD)
    FiltBankValues=filter_banks(np.transpose(PowerSpect), fs, nfilt=40, NFFT=512)
    #MFCCsVectors=dct(FiltBankValues, type=2, axis=1, norm='ortho')
    # 7. of the obtaine vector or vectors? only the first 13 elements are kept
    