import math
import numpy as np

def normalize(x): 
    """ normalize an input signal
        arguments: 
            x: input signal
        returns:
            xNormalized: normakized signal
            """
    Xmax = np.amax(np.abs(x)) # find maximum amplitude
    xNormalized = x/Xmax # normalization
    
    return xNormalized

def framing(fs,sig):
    """ Cuts a signal into frames. is used everywhere except with Formants
    arguments:
        fs: sampling frequency
        sig: input signal
    returns:
        frameList: array-like containing the frames """
    width=25 # width of a frame in ms
    step=10 # step between 2 frames in ms
    duration = np.size(sig) # number of samples making the signal
    width = math.floor(width*fs/1000) # convert into number of samples
    step = math.floor(step*fs/1000) # convert into number of samples
    framelist=[]
    f=0 # first sample of the frame
    l=0 # last sample of the frame

    if duration <= width:
        numframes = 1
    else:
        numframes = 1 + int(math.ceil((1.0 * duration - width) / step))

    padlen = int((numframes - 1) * step + width)

    zeros = np.zeros((padlen - duration,))
    sig = np.concatenate((sig, zeros)) # adds zeros to the end of the signal and gives it an appropriate shape for all the frames to ahve the same length
    
    itmax=int(duration/step)-1
    for j in range(0,itmax):
        l=f+width
        temp=np.asarray(sig[f:l])
        framelist.append(temp) # ajoute une frame à la liste
        f=f+step
    framelist=np.asarray(framelist)
    
    return framelist

def framing2(fs,sig):
    """ Cuts a signal into frames. is used with formants
    arguments:
        fs: sampling frequency
        sig: input signal
    returns:
        frameList: array-like containing the frames """
    
    width=25 # width of a frame in ms
    step=10 # step between 2 frames in ms
    duration = np.size(sig) # number of samples making the signal
    width = math.floor(width*fs/1000) # convert into number of samples
    step = math.floor(step*fs/1000) # convert into number of samples
    framelist=[]
    f=0 # first sample of the frame
    l=0 # last sample of the frame
    
    for j in range(0,duration,step): #duration, step or just itmax / formants or mfccs
        l=f+width
        temp=np.asarray(sig[f:l])
        framelist.append(temp) # ajoute une frame à la liste
        f=f+step
    del framelist[-1] # deletes last element
    framelist=np.asarray(framelist)
    return framelist
    

