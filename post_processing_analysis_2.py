# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

class plots():
   def __init__(self, data, shape = (2,2), figsize = (10,5)):
       
       def unit_circle(data):
           r = np.mean(abs(data))
           dI = np.arange(360)*2*np.pi/360
           xc = np.sin(dI)
           yc = np.cos(dI)
           x = xc * r
           y = yc * r
           return x, y
               
       avg_ang = np.angle(np.mean(data, axis = -1))
       data = data*np.exp(-1j*avg_ang)
       
       self.data = data 
       self.iq_real = np.real(data)
       self.iq_img = np.imag(data)
       self.iq_real_lpf = []
       self.iq_img_lpf = []
       self.circ = unit_circle(data)
       self.std = 'Not yet defined'
       self.data_lp = []
       self.fig = plt.figure(figsize=figsize)
       self.lpplot = False
       self.i = 1 
       self.nrow = shape[0]
       self.ncol = shape[1]
       self.samp_rate = (122.07*10**3)
       
       
   def plotiq(self):
       
        ax1 = self.fig.add_subplot(self.nrow, self.ncol,self.i)
        ax1.plot(self.iq_real, self.iq_img,'b.', self.circ[0], self.circ[-1],'c-')
        plt.axis('equal')
        ax1.set_title('No filter IQ')
        
       
   def plot_iq_lpf(self):
       def butter_lowpass(lowcut, fs, order = 3):
           nyq = 0.5 * fs
           low = lowcut / nyq
           b,a = sig.butter(order, low, btype='low',analog=False)
           return b,a  

       def lpf(data):
           b,a = butter_lowpass(1025, self.samp_rate)
           lpf_iq = sig.filtfilt(b,a, data)
           return lpf_iq
       
       self.i = 2
       self.data_lp = lpf(self.data)
       self.iq_real_lpf = np.real(self.data_lp)
       self.iq_img_lpf = np.imag(self.data_lp)
       
       ax1 = self.fig.add_subplot(self.nrow, self.ncol,self.i)
       ax1.plot(self.iq_real_lpf, self.iq_img_lpf,'b.', self.circ[0], self.circ[-1],'c-')
       plt.tight_layout()
       plt.axis('equal')
       ax1.set_title('LPF IQ')
       
   def hist(self):
       self.std = np.std(self.data)
       self.i = 3
       ax1 = self.fig.add_subplot(self.nrow, self.ncol,self.i)
       ax1.hist(self.data, bins = 100)
       ax1.set_title('No filter histogram; STD = {:.4f}'.format(self.std))
       
   def hist_lpf(self):
       self.std = np.std(self.data_lp)
       self.i = 4
       ax1 = self.fig.add_subplot(self.nrow, self.ncol,self.i)
       ax1.hist(self.data_lp, bins = 100)
       ax1.set_title('LPF histogram; STD = {:.4f}'.format(self.std))    

if __name__ == "__main__":
       
    i = np.load('I_1kHz_test2.npy')
    q = np.load('Q_1kHz_test2.npy')
    
    samp_rate = (122.07*10**3)             #sampling rate of Red Pitaya at 1024x decimation.
    dt = 1/samp_rate
    
    iq = i + 1j*q                         
        
    ds1 = plots(iq)
        
    ds1.plotiq()
    ds1.plot_iq_lpf()   
    ds1.hist()
    ds1.hist_lpf()
    plt.tight_layout()   