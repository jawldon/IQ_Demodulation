# -*- coding: utf-8 -*-

import numpy as np

def psd(data):
    N = len(data)                               #length of IQ complex128 data 
    x = data * np.hamming(len(data))            #apply Hamming window
    PSD = (np.abs(np.fft.fft(x))/N)**2          #normalized power spectral density
    PSD_log = 10.0*np.log10(PSD)
    PSD_shifted = np.fft.fftshift(PSD_log)
    return PSD_shifted

def freq(data, fs):
    N = len(data)                               #length of iq complex128 data
    f = np.arange(fs/-2.0, fs/2.0, fs/N)        # start, stop, step. Centered around 0 Hz
    return f

def disp(data):
    phase = np.angle(data)
    phase_unwrap = np.unwrap(phase)
    k = (1550/(4*np.pi))
    displacement = phase_unwrap*k
    return displacement[300:1_000]              #change slice as necessary 

def unit_circle(data):
    r = np.mean(abs(data))
    dI = np.arange(360)*2*np.pi/360
    xc = np.sin(dI)
    yc = np.cos(dI)
    x = xc * r
    y = yc * r
    return x, y