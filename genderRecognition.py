#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import os
import sys
import scipy.io.wavfile
from scipy.signal import decimate
from pylab import *
import numpy as np
from scipy import *
import warnings


MALE_VOICE_FREQ = 132.5
FEMALE_VOICE_FREQ = 210


def getFilesFromFolder(folder):
    return os.listdir(folder)


def randomGender():
    if(random.randint(0, 2) == 1): return "M"
    else: return "K"
    
    
def drawPlot(n, signal):
    fig = plt.figure(figsize = (15, 6), dpi = 80)   
    ax = fig.add_subplot(121)
    ax.plot(range(n), signal, linestyle = '-', color = 'red')
    show()
    
    
def drawFft(freqs, signal):
    fig = plt.figure(figsize = (15, 6), dpi = 80)
    ax = fig.add_subplot(122)
    ymax = max(signal)
    if (ymax > 3.0):
        ax.set_ylim([0.0,ymax])
    else:
        ax.set_ylim([0.0,3.0])
        
    stem(freqs, signal, '-*')
    show()
    

def getGenderByFreq(freq):
    if(abs(freq - MALE_VOICE_FREQ) <= abs(freq - FEMALE_VOICE_FREQ)): return "M"
    else: return "K"


def main(file):
    try:
        w, signal = scipy.io.wavfile.read(file)
    except:
        return randomGender()
    
    if(len(signal.shape) >= 2): signal = [s[0] for s in signal]
    
    n = len(signal)
    
    #drawPlot(n, signal)
    
    signalFft = scipy.fft.fft(signal)
    signalFft = abs(signalFft) / (0.5 * n)
    signalFft[0] = signalFft[0] / 2
    signalFft[0] = 0 #delete 0 - element
    
    freqs = [m / n * w for m in range(n)]
    
    index = int((1050 / w) * n)
    signalFft = signalFft[:index]
    freqs = freqs[:index]
    
    #drawFft(freqs, signalFft)
    
    signalFftDec = np.copy(signalFft)
    for p in range(2, 5):
        d = decimate(signalFft, int(p))
        signalFftDec[:len(d)] *= d
    
    #drawFft(freqs, signalFftDec)
    
    noiseIndex = int(105 / max(freqs) * len(freqs))
    signalFftDec[:noiseIndex] = 0
    
    #drawFft(freqs, signalFftDec)
    
    A = max(signalFftDec)
    fIndex = np.where(signalFftDec == A)[0][0]
    finalFreq = freqs[fIndex]
    
    #print(finalFreq)
    return getGenderByFreq(finalFreq)
   


'''folder = "waves/"
files = getFilesFromFolder(folder)
filesNumber = len(files)
results = 0

for file in files:
    gender = main(folder + file)
    #print(gender)
    if(file.split(".")[0][-1] == gender): results += 1

print(results / filesNumber)
'''
warnings.filterwarnings("ignore")

print(main(str(sys.argv[1])))


# In[ ]:




