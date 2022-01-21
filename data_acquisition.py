# -*- coding: utf-8 -*-
'''
Example data acquistion code for the Red Pitaya modified for our use. Code from:
https://redpitaya.readthedocs.io/en/latest/appsFeatures/examples/acqRF-exm1.html 
'''
import sys
import numpy as np
import red_pitaya_scpi_script as scpi
import matplotlib.pyplot as plt
import scipy.signal as signal
import struct
from matplotlib.animation import FuncAnimation
import matplotlib.animation as anim
import plots
import filters

fs = (122.07*10**3)              #sampling rate of Red Pitaya at 1024x decimation.

fig = plt.figure()
plt.subplots_adjust(left=0.155, bottom=0.035, right=0.9, top=0.96, wspace=0.2, hspace=0.35)
ax = fig.add_subplot(3,1,1)
ax1 = fig.add_subplot(3,1,2)
ax2 = fig.add_subplot(3,1,3)

def acq(data):
    rp_s1 = scpi.scpi('192.168.8.157')      #initiates connection with R.P. at this IP address
    rp_s2 = scpi.scpi('192.168.8.157')
    
    rp_s1.tx_txt('ACQ:DATA:FORMAT BIN')     #Formats data as BIN. 
    rp_s2.tx_txt('ACQ:DATA:FORMAT BIN')
    
    rp_s1.tx_txt('ACQ:DATA:UNITS VOLTS')    #Selects units in Volts for acquired data. 
    rp_s2.tx_txt('ACQ:DATA:UNITS VOLTS')
    
    rp_s1.tx_txt('ACQ:DEC 1024')            #Applies decimation factor to acquisition.
    rp_s2.tx_txt('ACQ:DEC 1024')
    
    rp_s1.tx_txt('ACQ:START')               #Starts aquisition.
    rp_s2.tx_txt('ACQ:START')
    
    rp_s1.tx_txt('ACQ:TRIG NOW')            #Sets for internal trigger. 
    rp_s2.tx_txt('ACQ:TRIG NOW')
    
    while 1:
        rp_s1.tx_txt('ACQ:TRIG:STAT?')      #Gets trigger status; triggers now. 
        if rp_s1.rx_txt() == 'TD':
            break
    while 1:
        rp_s2.tx_txt('ACQ:TRIG:STAT?')       
        if rp_s2.rx_txt() == 'TD':
            break
    
    rp_s1.tx_txt('ACQ:SOUR1:DATA?')         #Reads full data buffer starting from oldest sample at trigger. 
    rp_s2.tx_txt('ACQ:SOUR2:DATA?')
    
    buff_byte1 = rp_s1.rx_arb()             #Recieves binary data from scpi server.
    buff_byte2 = rp_s2.rx_arb()
    
    buff1 = [struct.unpack('!f',bytearray(buff_byte1[i:i+4]))[0] for i in range(0, len(buff_byte1), 4)]
    buff2 = [struct.unpack('!f',bytearray(buff_byte2[i:i+4]))[0] for i in range(0, len(buff_byte2), 4)]
    #unpack turns the binary data into a float, allowing us to plot these float values.
    #The '!f' refers to network big-endian byte order where the f refers to converting C struts into Python values, here it converts to a float. 
    
    np.save('I_1kHz_test2',buff1)
    np.save('Q_1kHz_test2', buff2)
    
    d,c = filters.butter_lowpass(1025, fs)         #create lowpass specs
    lp_iq1 = signal.lfilter(d, c, buff1)
    lp_iq2 = signal.lfilter(d, c, buff2)

    ax.clear()
    ax.plot(lp_iq1, label = 'I')
    ax.plot(lp_iq2, label = 'Q')
    ax.set_xlim([0, 2000])
    ax.set_ylim([-0.05, 0.05])
    ax.legend(loc = 'upper right', prop={'size': 15})
    ax.set_title('Demodulated Baseband IQ Signals', size = 15)
    ax.set_ylabel('Voltage (V)', size=12)
    ax.set_xlabel('Bins', size=12)
   
inter = 500   
ani = FuncAnimation(fig, acq, interval = inter)

def IQ(data):
    idata = np.load('I_1kHz_test2.npy')
    qdata = np.load('Q_1kHz_test2.npy')
    
    iqdata = idata + 1j*qdata
    avg_ang = np.angle(np.mean(iqdata, axis = -1))
    iqdata = iqdata * np.exp(-1j*avg_ang)
    
    d,c = filters.butter_lowpass(1025, fs)         #create lowpass specs
    lp_iq = signal.lfilter(d, c, iqdata)
    
    xx = plots.unit_circle(lp_iq)
    
    ax1.clear()
    ax1.plot(np.real(lp_iq), np.imag(lp_iq),'b.', xx[0], xx[-1],'c-')
    ax1.set_title('IQ Plot', size = 15)
    ax1.set_ylabel('Q', size=12)
    ax1.set_xlabel('I', size=12)
    ax1.axis('equal')
    
    '''FFT plot'''
    psd_lp = plots.psd(lp_iq)                   
    freq_lp = plots.freq(lp_iq, fs = fs)
    
    ax2.clear()
    ax2.plot(freq_lp, psd_lp)
    ax2.set_xlim(0, 10_000)
    ax2.set_ylabel('dB')
    ax2.set_title('PSD')

ani1 = FuncAnimation(fig, IQ, interval = inter)
plt.show()