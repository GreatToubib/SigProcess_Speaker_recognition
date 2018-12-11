from preprocess import framing
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
"""from scikits.talkbox import lpc"""

def hpfilter(fs,x): 
    #butter filter 
    N=1 #order
    cutoff_Hz=(fs*0.1) # cutoff frequency, frequencies below this will be deleted
    b,a =signal.butter(N,cutoff_Hz/(fs/2),'highpass') #butter filter
    print (b,a)
    xfiltered= signal.lfilter(b, a, x, axis=-1, zi=None) #apply filter to a signal
    
    plt.figure()
    plt.plot(xfiltered)
    plt.title("buttera")
    plt.show()
    return xfiltered

def hpfilter2(fs,x):
    #https://stackoverflow.com/questions/25107806/estimate-formants-using-lpc-in-python
    xfiltered=signal.lfilter([1., -0.67], [1.], x)
    plt.figure()
    plt.plot(x)
    plt.title("hp")
    plt.show()
    return xfiltered

def preEmphasis(fs,x,a):
    #simple application de la formule Formants, point 2.
    temp=np.zeros(len(x))
    
    i=1
    while i <= len(x)-2:
        temp[i-1]=x[i]-a*x[i-1]
        i=i+1
        
    plt.figure()
    plt.plot(temp)
    plt.title("emphasized")
    plt.show()
    
    return temp

def formant(fs,x):
    print("Formants")
    FL=np.asarray(framing(fs,x,30,15))
    a=0.63 #0,63 for pre emphasis
    i=0
    print(type(FL[i]))
    while i < len(FL):
        FL[i]=preEmphasis(fs, FL[i], a) # or other hp filter option ?
        w=signal.hamming(len(FL[i]))
        FL[i]= FL[i]*np.diag(w)
        """FL[i], e, k=lpc(FL[i],(2+fs/1000), axis=-1)"""
        
        """a : array-like
            the solution of the inversion.
        e : array-like
            the prediction error.
        k : array-like
            reflection coefficients.
        
        FL[i]=np.roots(FL[i]) #roots of the lpc's => the formants"""
        i=i+1
        
        
        """
        # Get LPC.
    A, e, k = lpc(x1, 8)

    # Get roots.
    rts = numpy.roots(A)
    rts = [r for r in rts if numpy.imag(r) >= 0]

    # Get angles.
    angz = numpy.arctan2(numpy.imag(rts), numpy.real(rts))

    # Get frequencies.
    Fs = spf.getframerate()
    frqs = sorted(angz * (Fs / (2 * math.pi)))"""