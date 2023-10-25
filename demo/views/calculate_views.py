import numpy as np
from scipy.interpolate import CubicSpline
from scipy import signal
import scipy
import matplotlib.pyplot as plt


import os 

from django.shortcuts import render
from django.views.generic.base import View


def read_dataset():
    files_path = 'media\\PPI\\'
    file_name_and_time_lst = []

    for f_name in os.listdir(f"{files_path}"):
        written_time = os.path.getctime(f"{files_path}{f_name}")
        file_name_and_time_lst.append((f_name, written_time))

    sorted_file_lst = sorted(file_name_and_time_lst, key=lambda x: x[1], reverse=True)


    if sorted_file_lst:  
        recent_file = sorted_file_lst[0]
        recent_file_name = recent_file[0]
        csv_dataset = os.path.join(files_path,recent_file_name)
    else:
        pass

    return csv_dataset


def dataset_IBI(data):
    data = np.genfromtxt(data, delimiter=',')
    data = np.nan_to_num(data, copy=False)

    # data=re.split('; |, |\*|\n|\t', data)
    IBI=[int(tmp)/128 for tmp in data]
    
    # print(IBI,"@@@@@")
    mIBI=sum(IBI)/len(IBI)
    if mIBI>400:
        IBI=[ibi/1000 for ibi in IBI]
    
    return IBI


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
    if np.all(np.diff(input)<=0):
        return -1
    
    return input

def anal_HRVtime(IBI):
    IBI=dataset_IBI(IBI)
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
    
    return '{:.1f}'.format(AVNN), '{:.1f}'.format(SDSD), '{:.1f}'.format(RMSSD), '{:.1f}'.format(pNNx)

def anal_HRVfreq(IBI):

    IBI = dataset_IBI(IBI)

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
    Fs_resamp=4
    IBI_resampled = signal.resample(IBI_interpolared, Fs_interp//Fs_resamp)
    
    # windowing (hanning)
    IBI_windowed=IBI_resampled*np.hanning(IBI_resampled.shape[0])
    
    # FFT 
    (freq, aY)=scipy.signal.welch(IBI_windowed, Fs_resamp, nperseg=len(IBI_windowed))  ##
        
    # Power Sum
    rangeVLF=[0.0033, 0.04]
    rangeLF=[0.04, 0.15]
    rangeHF=[0.15, 0.4]
    
    pTP=np.trapz(aY, freq)
    pVLF=np.trapz(aY[ (freq>=rangeVLF[0])&(freq>rangeVLF[1]) ], freq[ (freq>=rangeVLF[0])&(freq>rangeVLF[1]) ])
    pLF=np.trapz(aY[ (freq>=rangeLF[0])&(freq>rangeLF[1]) ], freq[ (freq>=rangeLF[0])&(freq>rangeLF[1]) ])
    pHF=np.trapz(aY[ (freq>=rangeHF[0])&(freq>rangeHF[1]) ], freq[ (freq>=rangeHF[0])&(freq>rangeHF[1]) ])
    
    pLF_HF=pLF/pHF
    nLF=pLF/(pTP-pVLF)
    nHF=pHF/(pTP-pVLF)
    return freq, aY, '{:.1f}'.format(pTP), '{:.1f}'.format(pVLF), '{:.1f}'.format(pLF), '{:.1f}'.format(pHF), '{:.1f}'.format(pLF_HF), '{:.1f}'.format(nLF), '{:.1f}'.format(nHF)



def show_analysis_result(request):
    dataset = read_dataset() 
    avnn, sdsd, rmssd, pnnx = anal_HRVtime(dataset)
    freq, aY, ptp, pvlf, plf, phf, plf_hf, nlf, nhf = anal_HRVfreq(dataset)



    fig, ax = plt.subplots(figsize=(6,4))
    plt.stem(freq, aY, 'b', markerfmt=" ", basefmt="-b")
    plt.ylabel('|Magnitude| (ms^2/Hz)')
    plt.xlabel('Frequency (Hz)')
    plt.tight_layout()
    plt.show()

   

    return render(request, 'demo/result.html', {
        'avnn_result': avnn,
        'sdsd_result': sdsd,
        'rmssd_result': rmssd,
        'pnnx_result': pnnx,
        'ptp_result': ptp,
        'pvlf_result': pvlf,
        'plf_result': plf,
        'phf_result': phf,
        'plf_hf_result': plf_hf,
        'nlf_result': nlf,
        'nhf_result': nhf,
    })


