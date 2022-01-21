# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal as sig 
import matplotlib.pyplot as plt
import scipy.signal as signal
import filters
import plots

'''
Signal analysis code for IQ demodulated data saved from Red Pitaya dual input channels. 
'''
i = np.load('I_1kHz_test2.npy')
q = np.load('Q_1kHz_test2.npy')

fs = (122.07*10**3)              #sampling rate of Red Pitaya at 1024x decimation.
dt = 1/fs

iq = i + 1j*q                    #combines i and q .npy files, converts to complex128
t = np.arange(iq.shape[-1])*dt   #time axis values

avg_ang = np.angle(np.mean(iq, axis = -1))
iq = iq*np.exp(-1j*avg_ang)

'''Filter settings'''

b,a = filters.butter_bandpass(975, 1025, fs)   #create bandpass specs
bp_iq = signal.lfilter(b, a, iq)

d,c = filters.butter_lowpass(1025, fs)         #create lowpass specs
lp_iq = signal.filtfilt(d, c, iq)

'''IQ plot settings'''

xx = plots.unit_circle(iq)

plt.figure()
plt.plot(np.real(iq), np.imag(iq),'b.', xx[0], xx[-1],'c-')
plt.axis('equal')


'''FFT settings'''

psd_bp = plots.psd(bp_iq)                   
freq_bp = plots.freq(bp_iq, fs = fs)

psd_iq = plots.psd(iq)
freq_iq = plots.freq(iq, fs = fs)

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax1.plot(freq_bp, psd_bp)
ax1.set_xlim(0, 10_000)
ax1.set_ylabel('dB')
ax1.set_title('975Hz-1025Hz, Bandpass Filter')

ax2 = fig.add_subplot(2,1,2)
ax2.plot(freq_iq, psd_iq)
ax2.set_xlim(0, 10_000)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('dB')
ax2.set_title('No Filter')
plt.show()

'''displacement'''

disp_iq = plots.disp(iq)
disp_lp = plots.disp(lp_iq)

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax1.plot(t[300:1_000], disp_lp)
ax1.set_ylabel('Displacement (nm)')
ax1.set_title('Displacement vs Time, Bandpass Filter')

ax2 = fig.add_subplot(2,1,2)
ax2.plot(t[300:1_000], disp_iq, 'g-')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Displacement (nm)')
ax2.set_title('No Filter')
plt.show()