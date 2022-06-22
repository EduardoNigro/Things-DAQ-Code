""" post_event_detection_level.py

Contains a usage example of find_cluster for level detection.

Read more at:
https://thingsdaq.org/2022/06/21/event-detection-in-signal-processing/

Author: Eduardo Nigro
    rev 0.0.1
    2022-06-21

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from utils import find_cluster

def make_fig():
    """
    Create figure and return axes for further plotting.
    
    """
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(6.3, 2.4),
        facecolor='#f8f8f8',
        tight_layout=True)
    # Adding and configuring axes
    ax = fig.add_subplot(
        xlim=(0, max(t)),
        xlabel='Time (s)',
        ylabel='Output ( - )',
        )
    ax.grid(linestyle=':')
    # Returning axes handle
    return ax

# "Continuous" signal parameters
tstop = 10  # Signal duration (s)
Ts0 = 0.0001  # Time step (s)
fs0 = 1/Ts0  # Sampling frequency (Hz)

# Creating arbitrary signal with multiple sine functions
freq = [1, 1.5, 2.3]  # Sine frequencies (Hz)
ampl = [1, 0.2, 0.4]  # Sine amplitude
t = np.arange(0, tstop+Ts0, Ts0)
x = np.zeros(len(t))
for ai, fi in zip(ampl, freq):
    x = x + ai*np.sin(2*np.pi*fi*t)
# Adding somewhat random noise to the signal
kn = 10  # Frequency multiplier
for _ in range(20):
    c = np.random.random(3)
    x = x + 0.04*c[0]*np.sin(2*np.pi*(kn*(freq[0]+kn*c[1]))*t + c[2])

# Discrete signal parameters
tsample = 0.01  # Sampling period for code execution (s)
fs = 1/tsample  # Sampling frequency (Hz)

# Finding a, b coefficients for butterworth digital filter
fc = 10  # Low-pass cutoff frequency (Hz)
b, a = signal.butter(1, fc, fs=fs)

# Preallocating variables
tn = []
xn = []
xcurr = 0

# Executing DAQ loop
tprev = 0
tcurr = 0
while tcurr <= tstop:
    # Doing I/O computations every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Simulating DAQ device signal acquisition
        xcurr = x[int(tcurr/Ts0)]
        # Updating output arrays
        tn.append(tcurr)
        xn.append(xcurr)
    # Updating previous values
    tprev = tcurr
    # Incrementing time step
    tcurr += Ts0

# Doing zero-phase digital filtering
xf = signal.filtfilt(b, a, xn, method='gust')

# Plotting raw and filtered signals
ax = make_fig()
ax.plot(tn, xn, linewidth=1.5, label='Raw', color='#1f77b4')
ax.plot(tn, xf, linewidth=1.5, label='Filtered', color='#ff7f0e')
ax.legend(loc='upper right')

# Plotting fitlered signal
ax = make_fig()
ax.plot(tn, xf, linewidth=1.5, label='Filtered', color='#ff7f0e', zorder=0)
# Finding and plotting positive peaks
imax = []
icl, ncl = find_cluster(xf>1, 1)
for ik, nk in zip(icl, ncl):
    imax.append(ik+np.argmax(xf[ik:ik+nk])-1)
    ax.scatter(tn[imax[-1]], xf[imax[-1]], s=25, c='#008800')
# Finding and plotting negative peaks
imin = []
icl, ncl = find_cluster(xf<-1, 1)
for ik, nk in zip(icl, ncl):
    imin.append(ik+np.argmin(xf[ik:ik+nk])-1)
    ax.scatter(tn[imin[-1]], xf[imin[-1]], s=25, c='#880000')
