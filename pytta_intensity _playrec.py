# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 18:01:24 2019

@author: Guto
"""
#%%
import pytta
import math as m
from pytta.classes import np
from pytta.classes import signal
from pytta.classes import plot

#%%
rho0 = 1.21
r = 37e-3
fs = 44100
sinFreq = 850
WWS = 44100/2
fftDegree = 18
#%%
t = np.linspace( 0, \
                (2**fftDegree/fs) \
                                          - (1/fs), \
                                      2**fftDegree) 
x1 = pytta.SignalObj(np.sin(2*m.pi*sinFreq*t), domain='time',samplingRate=fs)
x2 = pytta.SignalObj(np.sin(2*m.pi*sinFreq*t + (m.pi/2)), domain='time',samplingRate=fs)
#%%
ms = pytta.generate.measurement(kind='playrec',
                               excitation=x1,
                               device=24,
                               inChannel=[1],
                               outChannel=[1,2],
                               freqMin=20,
                               freqMax=20000,
                               samplingRate=fs)
#%% First mic measurement
m1 = ms.run()
#%% Second mic measurement
m2 = ms.run()
#%%
#a = signal.csd(m1.timeSignal,m2.timeSignal,fs=m.samplingRate)
S1 = signal.csd(np.squeeze(m1.timeSignal),np.squeeze(m2.timeSignal),fs=ms.samplingRate, nperseg = WWS)
I1 = -np.divide(np.imag(S1[1][1:]),S1[0][1:]*rho0*r)
#%%
plot.semilogx(S1[0][1:],10*np.log10(np.abs(I1)/10e-12))
 #%% First mic measurement
m3 = ms.run()
#%% Second mic measurement
m4 = ms.run()
#%%
#a = signal.csd(m1.timeSignal,m2.timeSignal,fs=m.samplingRate)
S2 = signal.csd(np.squeeze(m3.timeSignal),np.squeeze(m4.timeSignal),fs=ms.samplingRate, nperseg = WWS)
I2 = -np.divide(np.imag(S2[1][1:]),S2[0][1:]*rho0*r)
#%%
plot.semilogx(S2[0][1:],10*np.log10(np.abs(I2)/10e-12))