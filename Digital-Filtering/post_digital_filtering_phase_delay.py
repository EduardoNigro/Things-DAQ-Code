""" post_digital_filtering_phase_delay.py

Use this to explore regular and zero-phase filtering.

Read more at:
https://thingsdaq.org/2022/03/23/digital-filtering/

Author: Eduardo Nigro
    rev 0.0.1
    2022-03-23

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Creating general plotting function
def plot_general(x, y, x1=None, y1=None):
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(6.3, 2.8),
        facecolor='#f8f8f8',
        edgecolor='#f8f8f8',
        linewidth=3,
        tight_layout=True)
    # Adding and confguring axes
    ax = fig.add_subplot(
        xlim=(0, max(x)),
        xlabel='Time (s)',
        ylabel='Amplitude (V)',
        )
    ax.grid(
        linestyle=':'
        )
    # Plotting signals
    if x1 is None:
        ax.plot(x, y, linewidth=1.5, color='#1f77b4')
    else:
        ax.plot(x, y, linewidth=1.5, label='Raw', color='#1f77b4')
        ax.plot(x1, y1, linewidth=1.5, label='Filtered', color='#ff7f0e')
        ax.legend(loc='upper right')
        
# Creating time array for "continuous" signal
tstop = 2  # Signal duration (s)
Ts0 = 0.001  # "Continuous" time step (s)
fs0 = 1/Ts0  # "Continuous" sampling frequency (Hz)
t = np.arange(0, tstop+Ts0, Ts0)

# Creating low-pass Butterworth filter
fc = 10  # Cutoff frequency (Hz)
b0, a0 = signal.butter(1, fc, fs=fs0)

# Creating arbitrary signal with multiple sine waves
freq = [1, 1.5, 2.3]  # Sine frequencies (Hz)
ampl = [1, 0.2, 0.4]  # Sine amplitude
x = np.zeros(len(t))
for ak, fk in zip(ampl, freq):
    x = x + ak*np.sin(2*np.pi*fk*t)

# Adding somewhat random noise to the signal
kn = 10  # Frequency multiplier
xn = x  # Assigning base signal
for _ in range(20):
    c = np.random.random(3)
    xn = xn + 0.02*c[0]*np.sin(2*np.pi*(kn*(freq[0]+kn*c[1]))*t + c[2])

# Doing basic digital filtering
xf = signal.lfilter(b0, a0, xn)

# Doing zero-phase digital filtering
xfp = signal.filtfilt(b0, a0, xn, method='gust')

# Plotting signals
plot_general(t, xn, t, xf)
plot_general(t, xn, t, xfp)
