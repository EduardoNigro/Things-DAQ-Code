""" post_digital_filtering_butterworth.py

Contains a low-pass Butterworth digital filter.
You can use this to understand the effects of filter parameters.

Read more at:
https://thingsdaq.org/2022/03/23/digital-filtering/

Author: Eduardo Nigro
    rev 0.0.1
    2022-03-23

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# "Continuous" signal parameters
tstop = 1  # Signal duration (s)
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
yn = []
xcurr = 0  # x[n]
ycurr = 0  # y[n]
xprev = 0  # x[n-1]
yprev = 0  # y[n-1]

tprev = 0
tcurr = 0
# Executing DAQ loop
while tcurr <= tstop:
    # Doing I/O computations every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Simulating DAQ device signal acquisition
        xcurr = x[int(tcurr/Ts0)]
        # Filtering signal
        ycurr = -a[1]*yprev + b[0]*xcurr + b[1]*xprev
        yprev = ycurr
    # Updating output arrays
    tn.append(tcurr)
    xn.append(xcurr)
    yn.append(ycurr)
    # Updating previous values
    xprev = xcurr
    tprev = tcurr
    # Incrementing time step
    tcurr += Ts0

# Creating Matplotlib figure
fig = plt.figure(
    figsize=(6.3, 2.8),
    facecolor='#f8f8f8',
    tight_layout=True)
# Adding and configuring axes
ax = fig.add_subplot(
    xlim=(0, max(t)),
    xlabel='Time (s)',
    ylabel='Output ( - )',
    )
ax.grid(linestyle=':')
# Plotting signals
ax.plot(t, x, linewidth=1.5, label='Input', color='#1f77b4')
ax.plot(tn, yn, linewidth=1.5, label='Output', color='#ff7f0e')
ax.legend(loc='upper right')
