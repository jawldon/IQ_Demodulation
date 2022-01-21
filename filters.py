# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 14:34:56 2022

@author: jweldon
"""

import scipy.signal as signal

def butter_bandpass(lowcut, highcut, fs, order = 3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut /nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def butter_lowpass(lowcut, fs, order = 5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    c, d = signal.butter(order, low, btype='low',analog=False)
    return c, d