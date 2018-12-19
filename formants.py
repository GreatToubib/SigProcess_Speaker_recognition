from preprocess import framing2
from scipy import signal
import numpy as np
from lpc import lpc_ref as lpc

def hpfilter(fs,x): 
    """application of a butter filter( set up as an high pass filter) to a signal x
        arguments : 
            fs= sampling frequency
            x= signal
        returns : xfiltered= the filtered signal """
        
    N=1 #order = 1 for first order
    cutoff_Hz=(fs*0.1) # cutoff frequency, frequencies below this will be deleted
    b,a =signal.butter(N,cutoff_Hz/(fs/2),'highpass') #butter filter
    print (b,a)
    xfiltered= signal.lfilter(b, a, x, axis=-1, zi=None) #apply filter to a signal
    
    return xfiltered

def preEmphasis(x,a):
    """ Pre emphasize a signal: equivalent of passing it through a high pass filter
        arguments:
            x= signal
            a= preemphasis coefficient: 0 is no filter.
        returns: 
            xEmphasized: pre-emphasized signal"""
    xEmphasized=np.zeros(len(x))
    
    i=1
    while i <= len(x)-2:
        xEmphasized[i-1]=x[i]-a*x[i-1]
        i=i+1
        
    return xEmphasized

def formant(fs,x):
    """ returns the formants of an input signal.
        arguments: 
            fs: sampling frequency
            x: input signal
        returns:
            Formants: array-like of Formants ( only the first 4 )"""
            
    frameList=framing2(fs,x)
    #a=0.63 for pre emphasis
    i=0
    a=0.67
    while i < len(frameList):
        frameList[i]=preEmphasis(frameList[i],a) # gives same result as hpfilter function above
        w=signal.hamming(len(frameList[i])) # computes a hamming window of the desired shape
        frameList[i]= w*frameList[i] # applies the hamming window
        frameList[i]=lpc(frameList[i],int(2+fs/1000)) # applies lpc
        
        
        rts=np.roots(frameList[i]) #roots of the lpc's => the formants
        rts = [r for r in rts if np.imag(r) >= 0] #♦ keep only one conjugate
        angz = np.arctan2(np.imag(rts), np.real(rts)) # returns the corresponding angles
        frqs = sorted(angz * (fs / (2 * np.pi))) # returns the corresponding frequencies 
        frameList[i]=frqs # input the formants in our framelist
        frameList[i]=frameList[i][2:6]# keep only 4 values, i don't know why the 2 first values are always 0
        i=i+1
    Formants=frameList
    return Formants