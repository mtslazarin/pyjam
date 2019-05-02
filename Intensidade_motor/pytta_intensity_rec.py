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
r = 15.7e-3
fs = 44100
WWS = 40000 # Welch window size
fftDegree = 20
medicao='Carro'
#%% Setup de calibração
calibms = pytta.generate.measurement(kind='rec',
                                     lengthDomain='samples',
                                     fftDegree=18,
                                     device=4,
                                     inChannel=[1],
                                     samplingRate=fs,
                                     comment='calibração')
#%% Calibrações
calib = {}
#%%  Calibração
ch = 2
#calibms.channelName=['DG']
calibms.channelName=['DL']
calibms.inChannel = [ch]
calibration = calibms.run()
#%% Salva calibração
calib[calibms.channelName[0]] = calibration
#%% Setup medição 
ms = pytta.generate.measurement(kind='rec',
                                lengthDomain='samples',
                                fftDegree=fftDegree,
                                device=4,
                                inChannel=[1,2],
                                channelName=['DG','DL'],
                                samplingRate=fs,
                                comment=medicao)
#%% ----------
#%% Medições
Is = []
#%% Medindo 
med = ms.run()
#%% Split chs
medDG = pytta.SignalObj(med.timeSignal[:,0],samplingRate=fs,channelName=[med.channelName[0]])
medDL = pytta.SignalObj(med.timeSignal[:,1],samplingRate=fs,channelName=[med.channelName[1]])
#%% Aplicando calibração
medDG.calibPressure(calib['DG'],referencePressure=1)
medDL.calibPressure(calib['Channel 1'],referencePressure=1)
#%% Juntando novamente
medC = pytta.merge(medDG,medDL)
#%%
#a = signal.csd(m1.timeSignal,m2.timeSignal,fs=m.samplingRate)
S = signal.csd(np.squeeze(medC.timeSignal[:,0]),np.squeeze(medC.timeSignal[:,1]),fs=fs, nperseg = WWS)
I = -np.divide(np.imag(S[1][1:]),S[0][1:]*rho0*r)
#%%
IsigObj = pytta.SignalObj(I,domain='freq',unit='W/m2',samplingRate=fs)
#%% Conferes do espectro
IsigObj.plot_freq()
#%% Nome do take
IsigObj.comment
#%% Salvando na lista de medições
Is.append(IsigObj)