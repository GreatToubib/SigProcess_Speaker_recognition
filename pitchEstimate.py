from energy import energy
from preprocess import normalize,framing
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt



def xCorrF0(xFrame,fs):
    
    """  returns fundamental frequency of a frame using xcorr
        arguments: xFrame = one frame of the signal
                    fs= sampling frequency
            returns F0: fundamental frequency of the frame"""
    
    F0=0
    lags,c, line, b=plt.xcorr(xFrame, xFrame, normed=True, usevlines=True, maxlags=320) # c = taux de correlation, l'ordonnée. 50Hz => 320
    peaks, _=signal.find_peaks(c)
    middleIndex = int((np.size(peaks) - 1)/2)
    if(np.size(peaks) != 1):
        F0=(peaks[middleIndex+1]-peaks[middleIndex])
        """ peaks donne les positions des peaks ! donc position milieu +1 - position du milieu = f0 """
        
    return F0

def cepstrumF0(xFrame,fs):
    
    """  returns fundamental frequency of a frame using cepstrum
         arguments: xFrame = one frame of the signal
                    fs= sampling frequency
            returns F0: fundamental frequency of the frame"""
    F0=0
    
    w, h = signal.freqz(xFrame)
    h=np.fft.ifft(20 * np.log10(abs(h)))# The frequency response, as complex numbers.
    
    peaks, _=signal.find_peaks(h)
    peaksvalues=[]
    
    for i in range (10,len(peaks)-10,1):
       peaksvalues.append(h[i]) 

    F0=np.argmax(peaksvalues)
    
    return F0

def findPitch(fs,x,method):
    """ returns all the fundamental frequencies ( for each frame of the signal )
    arguments:
        fs: sampling frequency
        x : the signal 
        method: 0 to use autocorrelation, 1 to use cepstrum based algorithm
    returns: 
        F0s: array like, contains the fundamental frequency of each frame """
        
    x=normalize(x)
    FL=framing(fs,x)
    VorU= [] #voice or unvoiced frame?
    F0s=[] 
    threshold = 7 
    """We observed and listened to 5 random signals. 
    We noticed that most of voiced sounds gave a corresponding energy superior to 7."""
    for i in range (0,len(FL)):
        Ef=energy(FL[i]) 
        if method ==1:
            w=signal.hamming(len(FL[i]))
            FL[i]= w*FL[i]
        if Ef > threshold:
            VorU.append(1) # voiced
            if method==0: F0s.append(xCorrF0(FL[i],fs))
            if method==1: F0s.append(cepstrumF0(FL[i],fs))
        else:
            VorU.append(0) # unvoiced
            F0s.append(0)
    F0s=np.asarray(F0s)        
    return F0s        
