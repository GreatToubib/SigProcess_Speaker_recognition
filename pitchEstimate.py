from energy import energy
from preprocess import normalize,framing
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



def estimateF0(xFrame,fs):
    #autocorr Based
    
    F0=0
    lags,c, line, b=plt.xcorr(xFrame, xFrame, normed=True, usevlines=True, maxlags=320) # c = taux de correlation, l'ordonnée. 50Hz => 320
    plt.title("xcorr empilement")
    #affichage chelou, ils s'empilent tous?
    peaks, _=signal.find_peaks(c)
    middleIndex = int((np.size(peaks) - 1)/2)
    if(np.size(peaks) != 1):
        F0=(peaks[middleIndex+1]-peaks[middleIndex])
        """ peaks donne les positions des peaks ! donc position milieu +1 - position du milieu = f0 """
        
    return F0

def autocorrBasedpitch(fs,x):
    x=normalize(x)
    FL=np.asarray(framing(fs,x,30,15))
    E=[]
    VorU= [] #voice or unvoiced frame?
    F0s=[]
    threshold = 7
    for i in range (0,len(FL)):
        Ef=energy(FL[i])
        E.append(Ef)
        if Ef > threshold:
            VorU.append(1) # voiced
            F0s.append(estimateF0(FL[i],fs))
        else:
            VorU.append(0) # unvoiced
            F0s.append(0)
    F0s=np.asarray(F0s)        
    """plt.figure()
    plt.subplot(2,1,1)
    plt.plot(E) # energie 
    plt.title("Energie par Frame")
    plt.show()
    plt.subplot(2,1,2)
    plt.plot(VorU) # voiced or unvoiced
    plt.title("Voiced/unvoiced frame?")
    plt.show()
    plt.figure()
    plt.plot(F0s) # frequences fondamentales
    plt.title("fréquences fondamentales par frame: autocorr")
    plt.show()"""
    return F0s        
    
    
def SestimateF0(xFrame,fs):
    F0=0
    
    w, h = signal.freqz(xFrame)
    h=np.fft.ifft(20 * np.log10(abs(h)))# The frequency response, as complex numbers.
    """h=20 * np.log10(abs(h)) """ #spectrum
    f=w*fs/(2*np.pi) 
    
    peaks, _=signal.find_peaks(h)
    #on est dans un domaine temporel
    peaksvalues=[]
    for i in range (10,len(peaks)-10,1):
       peaksvalues.append(h[i]) 

    F0=np.argmax(peaksvalues)
    return F0

def cepstrumBasedPitch(fs,x):
    x=normalize(x)
    FL=framing(fs,x,30,15)
    E=[]
    VorU= [] #voice or unvoiced frame?
    F0s=[]
    threshold = 7
    for i in range (0,len(FL)):
        Ef=energy(FL[i])
        E.append(Ef)
        """w=signal.hamming(len(FL[i]))
        FL[i]= w*FL[i]"""
        if Ef > threshold:
            VorU.append(1) # voiced
            F0s.append(SestimateF0(FL[i],fs))
        else:
            VorU.append(0) # unvoiced
            F0s.append(0)
    F0s=np.asarray(F0s)   
    """plt.figure()
    plt.plot(F0s) # frequences fondamentales
    plt.title("fréquences fondamentales par frame: cepstrum")
    plt.show()"""
      
    return F0s  
    