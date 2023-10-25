import numpy as np
from scipy.interpolate import CubicSpline
from scipy import signal
from scipy.integrate import simps
import scipy
#import matplotlib.pyplot as plt

def check_ms(IBI):
    IBI=np.array(IBI)
    if np.mean(IBI)<400:
        IBI=np.round(IBI*1000)
    return IBI

def check_IBI(input):
    input=np.array(input)
    if input.shape[0]<10:
        return -1
    if np.all(input>2000):
        return -1
    if np.all(input<400):
        return -1
    if np.all(np.diff(input)>=0):
        return -1
    return input

def anal_HRVtime(IBI):
    IBI=check_ms(IBI)
    IBI=check_IBI(IBI)

    def calc_pNNx(dIBI, x=50):
        return 100*np.sum(np.abs(dIBI)>x)/dIBI.shape[0]
   
    IBI = np.array(IBI)
    dIBI = np.diff(IBI)
    
    AVNN = np.mean(IBI)
    SDSD = np.std(dIBI)
    RMSSD = np.sqrt(np.mean(dIBI*dIBI))
    pNNx = calc_pNNx(dIBI, x=50)
    
    #print('AVNN:', '{:6.2f}'.format(AVNN), 'SDSD:', '{:6.2f}'.format(SDSD), 'RMSSD:', '{:6.2f}'.format(RMSSD), 'pNNx:', '{:6.2f}'.format(pNNx))

    return '{:.1f}'.format(AVNN), '{:.1f}'.format(SDSD), '{:.1f}'.format(RMSSD), '{:.1f}'.format(pNNx)

def anal_HRVfreq(IBI):
    IBI=check_ms(IBI)
    IBI=check_IBI(IBI)
    tonset=np.cumsum(IBI)
    
    # detrend
    IBI = signal.detrend(IBI)
    IBI = IBI - np.mean(IBI)
    
    # interpolation (1kHz)
    Fs_interp=1000
    cs = CubicSpline(tonset, IBI)
    tonset_interpolated = np.arange(tonset[0], tonset[-1], 1000/Fs_interp, dtype=int)
    IBI_interpolared=cs(tonset_interpolated)
    
    #plt.plot(tonset/1000, IBI, 'y', linewidth=5)
    #plt.plot(tonset_interpolated/1000, IBI_interpolared, 'k', linewidth=1)
    
    #print(tonset_interpolated)
    # resampling (4 Hz)
    Fs_resamp=4
    IBI_resampled = signal.resample(IBI_interpolared, Fs_interp//Fs_resamp)
    # windowing (hanning)
    IBI_windowed=IBI_resampled*np.hanning(IBI_resampled.shape[0])
    #plt.plot(IBI_windowed, 'k', linewidth=1)
    
    # FFT 
    
    (freq, aY)=scipy.signal.welch(IBI_windowed, Fs_resamp, nperseg=len(IBI_windowed))
        
    # Power Sum
    rangeVLF=[0.0033, 0.04]
    rangeLF=[0.04, 0.15]
    rangeHF=[0.15, 0.4]
    
    pTP=simps(aY, freq)
    pVLF=simps(aY[ (freq>=rangeVLF[0])&(freq>rangeVLF[1]) ], freq[ (freq>=rangeVLF[0])&(freq>rangeVLF[1]) ])
    pLF=simps(aY[ (freq>=rangeLF[0])&(freq>rangeLF[1]) ], freq[ (freq>=rangeLF[0])&(freq>rangeLF[1]) ])
    pHF=simps(aY[ (freq>=rangeHF[0])&(freq>rangeHF[1]) ], freq[ (freq>=rangeHF[0])&(freq>rangeHF[1]) ])
    
    pLF_HF=pLF/pHF
    nLF=pLF/(pTP-pVLF)
    nHF=pHF/(pTP-pVLF)
    
    #print('Total power:', '{:6.2f}'.format(pTP), 'VLF power:', '{:6.2f}'.format(pVLF), 'LF power:', '{:6.2f}'.format(pLF), 'HF power:', '{:6.2f}'.format(pHF), 'LF/HF:', '{:6.2f}'.format(pLF_HF), 'nLF:', '{:6.2f}'.format(nLF), 'nHF:', '{:6.2f}'.format(nHF))

    #plt.stem(freq, aY, 'b', markerfmt=" ", basefmt="-b")
    #plt.ylabel('|Magnitude| (ms^2/Hz)')
    #plt.xlabel('Frequency (Hz)')
    #plt.rcParams['figure.figsize'] = [4, 4]
    #plt.show()

    #return pTP, pVLF, pLF, pHF, pLF_HF, nLF, nHF
    return freq, aY, '{:.1f}'.format(pTP), '{:.1f}'.format(pVLF), '{:.1f}'.format(pLF), '{:.1f}'.format(pHF), '{:.1f}'.format(pLF_HF), '{:.1f}'.format(nLF), '{:.1f}'.format(nHF)
